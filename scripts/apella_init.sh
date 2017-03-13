#!/bin/sh

CONFIGBASE=/etc/apella
RESOURCES=/usr/lib/apella/resources
DATADIR=/var/lib/apella/data

cmd () {
    echo " "
    echo "--- $@"
    "$@"
}

cmd apella run-installation-validations

cmd apella migrate

cmd apella loadinstitutions "${RESOURCES}/institutions.csv"
cmd apella loadschools "${RESOURCES}/schools.csv"
cmd apella loaddepartments "${RESOURCES}/departments.csv"
cmd apella loadsubjects "${RESOURCES}/subject_areas_subjects.csv"

#cmd apella user-add \
#        --username 'charitini' \
#        --password-from-json "${CONFIGBASE}/passwords" \
#        --first-name-el 'Χαριτίνη' \
#        --first-name-el 'Charitini' \
#        --last-name-el 'Μπλιάτσιου' \
#        --first-name-en 'Charitini' \
#        --last-name-en 'Bliatsiou' \
#        --role 'helpdeskadmin' \
#        --father-name-en 'Athanasios' \
#        --email 'charitini@grnet.gr' \


cmd apella professor-rank-add \
    --rank-el 'Καθηγητής' \
    --rank-en 'Professor' \


cmd apella professor-rank-add \
    --rank-el 'Αναπληρωτής Καθηγητής' \
    --rank-en 'Associate Professor' \


cmd apella professor-rank-add \
    --rank-el 'Επίκουρος Καθηγητής' \
    --rank-en 'Assistant Professor' \

cmd apella professor-rank-add \
    --rank-el 'Λέκτορας' \
    --rank-en 'Lecturer' \

for f in "${DATADIR}"/migrate_data/*.csv; do
    cmd apella loadmigrationdata "${f}"
done


apella shell << EOF
from apella.migration_functions import migrate_institutions_metadata
migrate_institutions_metadata()
EOF
echo ' '
