\set positions_to_migrate `cat positions_to_migrate.txt`
copy (
select
    c.id candidacy_serial,
    p.id position_serial,
    r.user_id candidate_user_id,
    c.opentoothercandidates open_to_other_candidates,
    c.date submitted_at,
    case
        when c.withdrawn is true then c.withdrawndate
        else null
    end as withdrawn_at
from
    position p,
    positionphase pp,
    positioncandidacies pc,
    candidacy c,
    roles r
where
    pc.position_id = p.id
    and c.candidate_id = r.id
    and c.candidacies_id = pc.id
    and c.permanent is true
    and p.phase_id = pp.id
    and p.id in :positions_to_migrate
) to '/tmp/OldApellaCandidacyMigrationData.csv' with csv header delimiter ',';
