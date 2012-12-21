#!/bin/bash
# This is a Django, Project-specific Cron script.
# Separate Projects would need a copy of this script
# with appropriate Settings export statments.

#this'll run on an env macbook for linux shared youll need to cd to the env dir this line and next line: source ./bin/activate

export DJANGO_SETTINGS_MODULE=moviemachine.settings

echo $DJANGO_SETTINGS_MODULE

python run_crom.py