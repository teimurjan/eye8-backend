#!/bin/sh
heroku container:push web --app bigsty
heroku container:release web --app bigsty