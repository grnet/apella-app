import os
import logging
from django.conf import settings
from apella.util import safe_path_join


logger = logging.getLogger()


def validate_installation():
    validate_logger()
    validate_old_file_permissions()
    validate_new_file_permissions()


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
            with open(write_test_path, "w") as f:
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
                with open(read_test_path, "r") as f:
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
