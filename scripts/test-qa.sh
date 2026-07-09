#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export ENV=qa
# export ENV=${1:-qa}
# export ENV=${ENV:-qa}

"$SCRIPT_DIR/helpers/pytest.sh" "$@"