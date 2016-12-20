#!/bin/sh

CONFIGBASE=/etc/apella
RESOURCES=/usr/lib/apella/resources

apella loadinstitutions "${RESOURCES}/institutions.csv"
apella loadschools "${RESOURCES}/schools.csv"
apella loaddepartments "${RESOURCES}/departments.csv"
apella loadsubjects "${RESOURCES}/subject_areas_subjects.csv"

apella user-add \
        --username 'charitini' \
        --password-from-json "${CONFIGBASE}/passwords" \
        --first-name-el 'Χαριτίνη' \
        --first-name-el 'Charitini' \
        --last-name-el 'Μπλιάτσιου' \
        --first-name-en 'Charitini' \
        --last-name-en 'Bliatsiou' \
        --role 'helpdeskadmin' \
        --father-name-en 'Athanasios' \
        --email 'charitini@grnet.gr' \


apella professor-rank-add \
    --rank-el 'Καθηγητής' \
    --rank-en 'Professor' \


apella professor-rank-add \
    --rank-el 'Αναπληρωτής Καθηγητής' \
    --rank-en 'Associate Professor' \


apella professor-rank-add \
    --rank-el 'Επίκουρος Καθηγητής' \
    --rank-en 'Assistant Professor' \
