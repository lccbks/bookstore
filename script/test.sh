#!/bin/sh
export PATHONPATH=`pwd`
#coverage run --timid --branch --source fe,be --concurrency=thread -m pytest -v --ignore=fe/data
coverage run --source=. -m pytest
coverage combine
coverage report
coverage html