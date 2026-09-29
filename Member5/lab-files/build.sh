#!/usr/bin/env bash
# Run inside the SEED VM with: bash build.sh
set -euo pipefail
cd -- "$(dirname -- "$0")"
if [[ $(id -u) == 0 ]]; then
    echo "Run as seed, without sudo; only ownership setup below uses sudo." >&2
    exit 1
fi
if [[ $(uname -s) != Linux ]]; then
    echo "These programs require the SEED Linux VM." >&2
    exit 1
fi
# Remove our old binaries first, since previous builds are owned by root.
# The workspace must be a private directory owned by seed.
rm -f -- vulp vulp_slow vulp_least attack_naive attack_atomic
gcc -Wall -Wextra -O0 vulp.c -o vulp
gcc -Wall -Wextra -O0 -DDEMO_DELAY=10 vulp.c -o vulp_slow
gcc -Wall -Wextra -O0 -DLEAST_PRIVILEGE vulp.c -o vulp_least
gcc -Wall -Wextra -O2 attack_naive.c -o attack_naive
gcc -Wall -Wextra -O2 attack_atomic.c -o attack_atomic
sudo chown root:root vulp vulp_slow vulp_least
sudo chmod 4755 vulp vulp_slow vulp_least
chmod 755 attack_naive attack_atomic
ls -l vulp vulp_slow vulp_least attack_naive attack_atomic
echo "Built. Victims should show root ownership and -rwsr-xr-x."
