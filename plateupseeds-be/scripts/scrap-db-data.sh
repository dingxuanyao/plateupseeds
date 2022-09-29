#!/usr/bin/env bash
# This script is used to delete all data from the database.

DB_NAME="plateup"
DB_USER="tonyyao"


delete_db_data() {
  echo "Deleting all data from the database..."
  for table in users likes seeds; do
    psql -d $DB_NAME -U $DB_USER -c "DROP TABLE $table CASCADE;"
  done

  echo "Done."
}

delete_db_data
