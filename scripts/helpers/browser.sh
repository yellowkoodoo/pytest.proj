#!/bin/bash

get_default_browser() {
    python -c "from config.settings import runnerSettings; print(runnerSettings.DEFAULT_BROWSER.value)"
}

get_default_headless() {
    python -c "from config.settings import runnerSettings; print(runnerSettings.DEFAULT_HEADLESS)"
}