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
            id,
            candidacy_id,
            null candidate_id
        from
            candidacyfile
        union
        select
            id,
            null candidacy_id,
            candidate_id
        from
            candidatefile
    ) cf,
    fileheader fh,
    filebody fb
where
    pc.position_id = p.id
    and pc.id = c.candidacies_id
    and (cf.candidacy_id = c.id or cf.candidate_id = c.candidate_id)
    and cf.id = fh.id
    and fh.currentbody_id = fb.id
    and fh.deleted is false
    and p.id in :positions_to_migrate
) to '/tmp/OldApellaCandidacyFileMigrationData.csv' with csv header delimiter ',';
