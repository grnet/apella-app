#!/bin/sh

for f in *.sql; do
        sed -i -- 's/and p.id in :positions_to_migrate/-- and p.id in :positions_to_migrate/' "$f"
done 
