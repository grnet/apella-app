copy (
select
    i.id as institution_id,
    irf.eswterikoskanonismosurl as institution_bylaw_url,
    irf.organismosurl as institution_organization_url
from
    institution i, institutionregulatoryframework irf
where
    i.id = irf.institution_id
) to '/tmp/OldApellaInstitutionMigrationData.csv' with csv header delimiter ',';
