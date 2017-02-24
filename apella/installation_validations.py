import os
import logging
from django.conf import settings
from apella.util import safe_path_join
from apella.models import ApellaFile
from shutil import move


logger = logging.getLogger()


def validate_installation():
    validate_logger()
    validate_old_file_permissions()
    validate_new_file_permissions()
    validate_apella_files_related_names()


def validate_old_file_permissions():
    euid = os.geteuid()
    newroot = settings.MEDIA_ROOT
    oldroot = settings.OLD_APELLA_MEDIA_ROOT
    dircount = 0
    filecount = 0
    for dirpath, dirnames, filenames in os.walk(oldroot):
        dircount += 1
        for filename in filenames:
            filecount += 1
            if filecount & 1023 == 0:
                m = "Validated %d old files so far" % filecount
                logger.info(m)
            path = safe_path_join(dirpath, filename)
            owner = os.stat(path).st_uid
            if owner != euid:
                m = ("{path!r}: owner {owner!r} is not the same as "
                     "the running euid {euid!r}. "
                     "Hard linking from {oldroot!r} to {newroot!r} will fail.")
                m = m.format(path=path, owner=owner, euid=euid,
                             oldroot=oldroot, newroot=newroot)
                logger.error(m)
                raise RuntimeError(m)

    m = ("{path!r}: validated {filecount!r} old files "
         "in {dircount!r} directories")
    m = m.format(path=oldroot, filecount=filecount, dircount=dircount)
    logger.info(m)


def validate_new_file_permissions():
    newroot = settings.MEDIA_ROOT
    dircount = 0
    filecount = 0
    for dirpath, dirnames, filenames in os.walk(newroot):
        dircount += 1
        write_test_path = safe_path_join(dirpath, '..write_test')
        try:
            with open(write_test_path, "w"):
                try:
                    os.unlink(write_test_path)
                except Exception as e:
                    logger.error(e)
        except Exception as e:
            m = "{path!r}: cannot write in directory: {e!r}"
            m = m.format(path=dirpath, e=e)
            logger.error(m)
            raise RuntimeError(m)

        for filename in filenames:
            filecount += 1
            if filecount & 1023 == 0:
                m = "Validated %d old files so far" % filecount
                logger.info(m)
            read_test_path = safe_path_join(dirpath, filename)
            try:
                with open(read_test_path, "r"):
                    pass
            except Exception as e:
                m = "{path!r}: cannot open file for reading: {e!r}"
                m = m.format(path=read_test_path, e=e)
                logger.error(m)
                raise RuntimeError(m)

    m = ("{path!r}: validated {filecount!r} new files "
         "in {dircount!r} directories")
    m = m.format(path=newroot, filecount=filecount, dircount=dircount)
    logger.info(m)


def validate_logger():
    if not logger.handlers:
        m = "No handlers found for root logger."
        raise RuntimeError(m)

    filehandler = False
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            filehandler = True

        try:
            m = "Root logger at {name!r}"
            m = m.format(name=handler.stream.name)
            logger.info(m)
            print(m)
        except Exception as e:
            logger.exception(e)

    if not filehandler:
        m = ("No FileHandler found for root logger. "
             "Apella must have a log file on disk.")
        raise RuntimeError(m)


def validate_apella_files_related_names():
    af = ApellaFile.objects.all()[0]
    nr_related_managers = 0
    for name in dir(af):
        if name == 'objects':
            continue
        attr = getattr(af, name)
        if type(attr).__name__.endswith('RelatedManager'):
            nr_related_managers += 1
            if not (name.endswith('_file') or name.endswith('_files')):
                if name in ('self_evaluation_report'):
                    continue
                m = ("ApellaFile.%s is a RelatedManager "
                     "but its name does not end in '_file' or '_files'. "
                     "This means that you will regret calling "
                     "remove_unreferenced_apella_files(). WARNING.")
                m %= name
                raise AssertionError(m)

    if not nr_related_managers:
        m = "This is not right. WARNING."
        raise AssertionError(m)


def move_unreferenced_disk_files(dest_root, force=False):
    path_join = os.path.join
    isdir = os.path.isdir
    makedirs = os.makedirs

    MEDIA_ROOT = settings.MEDIA_ROOT.rstrip('/')
    dest_root = dest_root.rstrip('/')

    db_files = ApellaFile.objects.all().values_list('file_content', flat=True)
    db_file_paths = set(path_join(MEDIA_ROOT, x) for x in db_files)
    disk_file_paths = []
    for dirname, directories, filenames in os.walk(MEDIA_ROOT):
        disk_file_paths.extend(path_join(dirname, f) for f in filenames)

    nr_checked = 0
    nr_to_move = 0
    nr_moved = 0
    nr_errors = 0

    for disk_file_path in disk_file_paths:
        if nr_checked & 1023 == 0:
            m = "nr_checked: %d, nr_to_move: %d, nr_moved: %d, nr_errors: %d"
            m %= (nr_checked, nr_to_move, nr_moved, nr_errors)
            logger.info(m)

        nr_checked += 1
        if disk_file_path in db_file_paths:
            continue

        nr_to_move += 1
        dest_file_path = \
            disk_file_path.replace(MEDIA_ROOT, dest_root, 1).rstrip('/')
        if not dest_file_path.startswith(dest_root):
            nr_errors += 1
            m = "NOT moving %r to %r" % (disk_file_path, dest_file_path)
            logger.info(m)
            continue

        m = "moving %r to %r" % (disk_file_path, dest_file_path)
        logger.info(m)
        if force:
            try:
                dest_dirname = dirname(dest_file_path)
                if not isdir(dest_dirname):
                    makedirs(dest_dirname)
                move(disk_file_path, dest_file_path)
                nr_moved += 1
            except Exception as e:
                logger.exception(e)
                nr_errors += 1
    m = "nr_checked: %d, nr_to_move: %d, nr_moved: %d, nr_errors: %d"
    m %= (nr_checked, nr_to_move, nr_moved, nr_errors)
    logger.info(m)


def remove_unreferenced_apella_files(force=False):

    validate_apella_files_related_names()

    nr_checked = 0
    to_remove = []

    for af in ApellaFile.objects.all():
        nr_checked += 1
        if nr_checked & 1023 == 0:
            m = "nr_checked %d, nr_to_remove: %d"
            m %= (nr_checked, len(to_remove))
            logger.info(m)

        for attr_name in (
                x for x in dir(af)
                if ((x.endswith('_files') or x.endswith('_file')) and
                    type(getattr(af, x)).__name__.endswith('RelatedManager'))
        ):
            if getattr(af, attr_name).count() > 0:
                break
        else:
            to_remove.append(af)

    m = "nr_checked %d, nr_to_remove: %d"
    m %= (nr_checked, len(to_remove))
    logger.info(m)

    if force:
        m = "Removing %d rows..." % len(to_remove)
        logger.info(m)

        for af in to_remove:
            af.delete()
