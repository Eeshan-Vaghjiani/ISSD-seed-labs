#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
if [[ $(uname -s) != Linux || $(id -u) == 0 ]]; then
    echo 'Build inside the SEED Linux VM as ordinary seed, without sudo.' >&2
    exit 1
fi
gcc -std=gnu99 -Wall -Wextra -O2 -pthread cow_attack.c -o cow_attack
gcc -std=gnu99 -Wall -Wextra -O2 cow_control.c -o cow_control
chmod 0755 cow_attack cow_control
ls -l cow_attack cow_control
echo 'No Set-UID installation is used for Dirty COW.'
