copy (
select
    r.user_id user_id,
    c.version,
    s.id sector_id,
    s.areaid area_id,
    s.subjectid subject_id,
    sn.area area_name,
    sn.subject subject_name,
    sn.locale locale,
    dep.id_list departments_id
from
    roles r
    inner join positionsearchcriteria c on (c.candidate_id = r.id)
    left outer join positionsearchcriteria_sector cs on (cs.positionsearchcriteria_id = c.id)
    left outer join (
        select c.id id, cast(array_agg(cd.departments_id) as text) id_list
        from
            positionsearchcriteria c,
            positionsearchcriteria_department cd
        where cd.positionsearchcriteria_id = c.id
        group by c.id
    ) dep on (dep.id = c.id)
    left outer join sector s on (s.id = cs.sectors_id)
    left outer join sector_name sn on (s.id = sn.sector_id)
) to '/tmp/OldApellaAreaSubscriptions.csv' with csv header delimiter ',';
