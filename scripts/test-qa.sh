#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export ENV=qa
# export ENV=${1:-qa}
# export ENV=${ENV:-qa}
export BASE_URL="http://localhost:3000"

"$SCRIPT_DIR/helpers/pytest.sh" "$@"