#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

source "$SCRIPT_DIR/browser.sh"
cd "$PROJECT_ROOT"


export BROWSER=${BROWSER:-$(get_default_browser)}
export HEADLESS=${HEADLESS:-$(get_default_headless)}

PYTEST_ARGS="--browser=$BROWSER"

if [ "$HEADLESS" = "true" ]; then
    PYTEST_ARGS="$PYTEST_ARGS --headless"
else
    PYTEST_ARGS="$PYTEST_ARGS --headed"
fi

pytest $PYTEST_ARGS "$@"