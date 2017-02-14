\set positions_to_migrate `cat positions_to_migrate.txt`
copy (
select
    c.id candidacy_serial,
    p.id position_serial,
    c.candidate_id candidate_user_id,
    fh.id file_id,
    fh.type as file_type,
    fb.storedfilepath file_path,
    fb.originalfilename original_name,
    case
        when fb.date is null then '1970-01-01'
        else fb.date
    end as updated_at
from
    position p,
    positioncandidacies pc,
    candidacy c,
    (   select
            id header_id,
            candidacy_id
        from
            candidacyfile
        union
        select
            fb.header_id header_id,
            cfb.candidacy_id candidacy_id
        from
            candidacy_filebody cfb,
            filebody fb
        where
            cfb.files_id = fb.id
    ) cf,
    fileheader fh,
    filebody fb
where
    pc.position_id = p.id
    and pc.id = c.candidacies_id
    and cf.candidacy_id = c.id
    and cf.header_id = fh.id
    and fb.header_id = fh.id
    and fh.deleted is false
    and p.id in :positions_to_migrate
) to '/tmp/OldApellaCandidacyFileMigrationData.csv' with csv header delimiter ',';
