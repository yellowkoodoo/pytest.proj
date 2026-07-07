#!/bin/bash

set -e

source scripts/helpers/browser.sh

export BROWSER=${BROWSER:-$(get_default_browser)}
export HEADLESS=${HEADLESS:-$(get_default_headless)}

PYTEST_ARGS="--browser=$BROWSER"

if [ "$HEADLESS" = "true" ]; then
    PYTEST_ARGS="$PYTEST_ARGS --headless"
else
    PYTEST_ARGS="$PYTEST_ARGS --headed"
fi

pytest $PYTEST_ARGS "$@"