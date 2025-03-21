#!/bin/bash
set -e

# Start MySQL in the background
docker-entrypoint.sh mysqld &

# Wait for MySQL to be ready
until mysqladmin ping -h"localhost" --silent; do
    echo "Waiting for MySQL to start..."
    sleep 2
done

echo "MySQL is ready, initializing database..."

# Run your setup script
mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" < /docker-entrypoint-initdb.d/setup_cricket_db.sql

# Keep container running
wait 