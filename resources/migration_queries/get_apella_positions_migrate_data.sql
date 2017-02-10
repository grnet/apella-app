\set positions_to_migrate `cat positions_to_migrate.txt`
copy (
select
    p.id position_serial,
    p.description description,
    p.name title,
    su.name subject_id,
    p.department_id department_id,
    p.createdby_id manager_id,
    s.areaid subject_area_code,
    s.subjectid subject_code,
    p.fek gazette_publication_url,
    p.feksentdate gazette_publication_date,
    case
        when pp.status = 'ENTAGMENI' then 'ENTAGMENI'
        when pp.status = 'ANAPOMPI' then 'ANAPOMPI'
        when pp.status = 'ANOIXTI' then 'ANOIXTI'
        when pp.status = 'STELEXOMENI' then 'STELEXOMENI'
        when pp.status = 'EPILOGI' then 'EPILOGI'
        when pp.status = 'CANCELLED' then 'CANCELLED'
    end state,
    pc.openingdate opening_date,
    pc.closingdate closing_date
from
    position p, positionphase pp, positioncandidacies pc, sector s, subject su
where
    p.phase_id = pp.id
    and p.sector_id = s.id
    and pc.position_id = p.id
    and p.phase_id = pp.id
    and p.permanent is true
    and p.subject_id = su.id
    and p.id in :positions_to_migrate
) to '/tmp/OldApellaPositionMigrationData.csv' with csv header delimiter ',';
