#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
cd "$JC_DATA_DIR"
SERVER_IP="$(sed -n 's/^server-ip=//p' server.properties | tail -1)"
for _ in {1..120}; do
  if ip -4 addr show tailscale0 2>/dev/null | grep -Fq "$SERVER_IP"; then break; fi
  sleep 2
done
ip -4 addr show tailscale0 2>/dev/null | grep -Fq "$SERVER_IP" || jc_die "Tailscale address $SERVER_IP is not available"
if [[ -f .runtime.json && -f server.jar ]]; then
  [[ -x "$JC_JAVA" ]] || jc_die 'Isolated Java 25 is missing; run deploy'
  exec nice -n 10 "$JC_JAVA" @user_jvm_args.txt -jar server.jar --bonusChest nogui
elif [[ -f run.sh ]]; then
  # Retained only to permit an explicit restart/backup of the preserved old server.
  exec bash ./run.sh nogui
else
  jc_die 'Server is not installed. Run ./jialiangcraft deploy.'
fi
