#!/bin/bash

set -e

export ENV=qa
# export ENV=${1:-qa}
# export ENV=${ENV:-qa}

scripts/helpers/pytest.sh