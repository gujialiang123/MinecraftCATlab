#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
cd "$JC_DATA_DIR"
[[ -f run.sh ]] || jc_die 'NeoForge is not installed. Run ./jialiangcraft deploy.'
SERVER_IP="$(sed -n 's/^server-ip=//p' server.properties | tail -1)"
for _ in {1..120}; do
  if ip -4 addr show tailscale0 2>/dev/null | grep -Fq "$SERVER_IP"; then break; fi
  sleep 2
done
ip -4 addr show tailscale0 2>/dev/null | grep -Fq "$SERVER_IP" || jc_die "Tailscale address $SERVER_IP is not available"
exec bash ./run.sh nogui
