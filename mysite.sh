#!/bin/bash

cd ~/python/projects/mysite
export DJANGO_SETTINGS_MODULE=config.settings.prod
export PYTHONPATH=~/python/mypakages
. ~/python/venvs/mysite/bin/activate

