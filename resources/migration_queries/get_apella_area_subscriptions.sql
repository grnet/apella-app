copy (
select
    r.user_id user_id,
    c.version,
    s.id sector_id,
    s.areaid area_id,
    s.subjectid subject_id,
    sn.area area_name,
    sn.subject subject_name,
    sn.locale locale
from
    positionsearchcriteria c,
    positionsearchcriteria_sector cs,
    sector s,
    sector_name sn,
    roles r
where
    r.id = c.candidate_id
    and c.id = cs.positionsearchcriteria_id
    and s.id = cs.sectors_id
    and s.id = sn.sector_id
    and c.candidate_id = r.id
) to '/tmp/OldApellaAreaSubscriptions.csv' with csv header delimiter ',';
