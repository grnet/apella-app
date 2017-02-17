copy (
select
    u.id user_id,
    u.password passwd,
    u.passwordsalt passwd_salt,
    u.shibbolethinfo_remoteuser as shibboleth_id,
    case
        when u.username = '' then 'user' || u.id
        when u.username is null then 'user' || u.id
        else u.username
    end as username,
    u.permanentauthtoken permanent_auth_token,
    case
        when r.discriminator = 'INSTITUTION_MANAGER' then 'institutionmanager'
        when r.discriminator = 'INSTITUTION_ASSISTANT' then 'assistant'
        when r.discriminator = 'PROFESSOR_DOMESTIC' then 'professor'
        when r.discriminator = 'PROFESSOR_FOREIGN' then 'professor'
        when r.discriminator = 'ADMINISTRATOR' and a.superadministrator is true then 'helpdeskadmin'
        when r.discriminator = 'ADMINISTRATOR' and a.superadministrator is false then 'helpdeskuser'
        when r.discriminator = 'CANDIDATE' then 'candidate'
        else r.discriminator
    end as role,
    r.status role_status,
    u.basicinfo_firstname name_el,
    u.basicinfo_lastname surname_el,
    u.basicinfo_fathername fathername_el,
    u.basicinfolatin_firstname name_en,
    u.basicinfolatin_lastname surname_en,
    u.basicinfolatin_fathername fathername_en,
    u.contactinfo_email email,
    u.contactinfo_mobile mobile,
    u.contactinfo_phone phone,
    u.identification person_id_number,
    p.is_foreign is_foreign,
    p.speakinggreek speaks_greek,
    rn.name professor_rank,
    p.institution_id professor_institution_id,
    p.institution_freetext professor_institution_freetext,
    p.department_id professor_department_id,
    p.fek professor_appointment_gazette_url,
    sf.name professor_subject_from_appointment,
    sg.name professor_subject_optional_freetext,
    p.profileurl professor_institution_cv_url,
    case
        when im.institution_id is not null then im.institution_id
        when ia.institution_id is not null then ia.institution_id
        else null
    end as manager_institution_id,
    im.verificationauthority manager_appointer_authority,
    im.verificationauthorityname manager_appointer_fullname,
    im.alternatebasicinfo_firstname manager_deputy_name_el,
    im.alternatebasicinfo_lastname manager_deputy_surname_el,
    im.alternatebasicinfo_fathername manager_deputy_fathername_el,
    im.alternatebasicinfolatin_firstname manager_deputy_name_en,
    im.alternatebasicinfolatin_lastname manager_deputy_surname_en,
    im.alternatebasicinfolatin_fathername manager_deputy_fathername_en,
    im.alternatecontactinfo_mobile manager_deputy_mobile,
    im.alternatecontactinfo_phone manager_deputy_phone,
    im.alternatecontactinfo_email manager_deputy_email

from
    roles r
    left outer join
        (   select
                pd.id id,
                pd.institution_id institution_id,
                null institution_freetext,
                pd.department_id department_id,
                pd.subject_id subject_id,
                pd.feksubject_id feksubject_id,
                pd.rank_id rank_id,
                null speakinggreek,
                p.profileurl profileurl,
                false is_foreign,
                pd.fek fek
            from professordomestic pd, professor p
            where
                p.id = pd.id
            union select
                pf.id id,
                null institution_id,
                pf.institution institution_freetext,
                null department_id,
                pf.subject_id subject_id,
                null feksubject_id,
                pf.rank_id rank_id,
                pf.speakinggreek speakinggreek,
                p.profileurl profileurl,
                true is_foreign,
                null fek
            from professorforeign pf, professor p
            where
                p.id = pf.id
        ) p on (p.id = r.id)
    left outer join rank on (rank.id = p.rank_id)
    left outer join (select * from rank_name where locale = 'en') rn on (rn.rank_id = rank.id)
    left outer join subject sg on (sg.id = p.subject_id)
    left outer join subject sf on (sf.id = p.feksubject_id)
    left outer join institutionmanager im on (im.id = r.id)
    left outer join institutionassistant ia on (ia.id = r.id)
    left outer join users u on (u.id = r.user_id)
    left outer join administrator a on (a.id = r.id)

where
    u.status = 'ACTIVE'
) to '/tmp/OldApellaUserMigrationData.csv' with csv header delimiter ',';
