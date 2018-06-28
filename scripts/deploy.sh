#!/bin/bash

# Oneworksite deployment script
# Usage: DEPLOY_NAME=XX ./deploy.sh

BASE_REPO=~/repos

function error {
    echo "!! Error: $*, aborting" 1>&2
    exit 1
}

function run {
    echo ">> $*"
    $* 2>&1 || error "\"$*\" failed"
}

[[ -n "$DEPLOY_NAME" ]] || error "\$DEPLOY_NAME not set"

r=$BASE_REPO/$DEPLOY_NAME
[[ -d "$r" ]] || error "$r does not exist"

echo "Deploying $DEPLOY_NAME..."

source virtualenvwrapper.sh
export DJANGO_SETTINGS_MODULE="config.settings.live"

run cd $r
run workon $DEPLOY_NAME
run python manage.py migrate --no-color
run python manage.py collectstatic --no-color --no-input

echo "Reloading app..."
run touch $(readlink -f wsgi.py)

echo "Done"
