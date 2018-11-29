#!/usr/bin/env bash
set -e
scp db-backup.sql training:db-backup.sql
rm db-backup.sql
