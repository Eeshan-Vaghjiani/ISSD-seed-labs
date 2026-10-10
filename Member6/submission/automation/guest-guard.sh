#!/usr/bin/env bash
# Shared checks for this repository's separate historical Member 6 guest.
# Source this file; it performs no action until a function is called.

m6_require_guest() {
    local arch release product
    arch=$(uname -m)
    if [[ $(uname -s) != Linux || ! $arch =~ ^i[3-6]86$ ]]; then
        echo "STOP: expected the 32-bit SEED guest; actual architecture=$arch." >&2
        return 1
    fi
    if [[ $(id -un) != seed || $(id -ru) == 0 || $(id -ru) != "$EUID" ]]; then
        echo 'STOP: use the ordinary seed login, with equal nonzero real/effective UIDs.' >&2
        return 1
    fi
    if ! command -v lsb_release >/dev/null; then
        echo 'STOP: lsb_release is unavailable; guest release cannot be checked.' >&2
        return 1
    fi
    release=$(lsb_release -rs)
    if [[ $(lsb_release -is) != Ubuntu || $release != 12.04 ]]; then
        echo "STOP: expected Ubuntu 12.04; actual release=$release." >&2
        return 1
    fi
    if [[ $(uname -r) != 3.5.0-37-generic ]]; then
        echo "STOP: intended historical kernel is 3.5.0-37-generic; actual=$(uname -r)." >&2
        echo 'Inspect the image and package before proceeding; do not upgrade/downgrade to guess a fix.' >&2
        return 1
    fi
    product=$(cat /sys/class/dmi/id/product_name) || return 1
    if [[ $product != VirtualBox ]]; then
        echo "STOP: expected this separate VirtualBox guest; DMI product=$product." >&2
        return 1
    fi
    if [[ $HOME != /home/seed ]]; then
        echo "STOP: unexpected seed home: $HOME" >&2
        return 1
    fi
}

m6_require_workspace() {
    local filesystem
    if [[ $(pwd -P) != /home/seed/issd-member6/lab-files ]]; then
        echo 'STOP: work in /home/seed/issd-member6/lab-files on native guest storage.' >&2
        return 1
    fi
    filesystem=$(df -PT . | awk 'NR == 2 {print $2}')
    case "$filesystem" in
        ext2|ext3|ext4|xfs|btrfs) ;;
        *) echo "STOP: unexpected workspace filesystem=$filesystem." >&2; return 1 ;;
    esac
    if [[ $(stat -c %u .) != "$(id -u)" ]]; then
        echo 'STOP: the workspace is not owned by the ordinary seed user.' >&2
        return 1
    fi
}

m6_no_process() {
    local pattern=$1 status=0 pids
    pids=$(pgrep -x "$pattern") || status=$?
    case $status in
        1) printf 'No matching process: %s\n' "$pattern" ;;
        0)
            echo "STOP: matching process remains: $pattern" >&2
            ps -p "${pids//$'\n'/,}" -o pid,ppid,ruid,euid,tty,args
            return 1 ;;
        *) echo "STOP: pgrep failed, exit=$status." >&2; return 1 ;;
    esac
}

m6_no_attacker() {
    m6_no_process cow_attack || return 1
    local status=0 pids
    pids=$(pgrep -f '[b]ash (\./)?run_trial\.sh') || status=$?
    case $status in
        1) echo 'No supplied trial wrapper is running.' ;;
        0)
            echo 'STOP: a supplied trial wrapper remains.' >&2
            ps -p "${pids//$'\n'/,}" -o pid,ppid,ruid,euid,tty,args
            return 1 ;;
        *) echo "STOP: wrapper process check failed, exit=$status." >&2; return 1 ;;
    esac
}
