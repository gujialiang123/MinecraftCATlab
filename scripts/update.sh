#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
"$JC_ROOT/scripts/build-client.sh"
"$JC_ROOT/scripts/backup.sh"
"$JC_ROOT/scripts/stop.sh"
"$JC_ROOT/scripts/deploy.sh"
"$JC_ROOT/scripts/validate.sh"
