#!/bin/sh
mkdir instance
# SQLite doesn't handle migrations, so rely on SQLAlchmy table creation
PATH=.venv/bin:$PATH
. .venv/bin/activate
if grep "sqlite://" $APP_CONFIG_FILE; then
  echo "SQLLite DB, so skipping db migrations";
else
  FLASK_APP=servicex/app.py flask db upgrade;
fi

gunicorn -b :5000 --workers=5 --threads=1 --timeout 120 --access-logfile - --error-logfile - "servicex:create_app()"
