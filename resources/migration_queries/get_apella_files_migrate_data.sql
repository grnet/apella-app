copy (
select
    u.id user_id,
    fh.id header_id,
    fh.type file_type,
    fh.description file_description,
    fb.storedfilepath file_path,
    fb.originalfilename original_name
from
    users u,
    fileheader fh,
    filebody fb
where
    fh.owner_id = u.id
    and fh.currentbody_id = fb.id
    and fh.deleted is false
order by user_id, header_id
) to '/tmp/OldApellaFileMigrationData.csv' with csv header delimiter ',';
