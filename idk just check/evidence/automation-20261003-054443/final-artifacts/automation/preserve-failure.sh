#!/usr/bin/env bash
# Source in terminal B before the first reset. No administrator operations.
preserve_failure() {
    local dest="$LAB_EVIDENCE/pre-reset-task2b"
    set -x
    id
    date -Is
    pgrep -a -x 'attack_naive|attack_atomic|vulp|vulp_slow|vulp_least|su'
    pgrep -af '[b]ash run_trials.sh'
    ls -ld /tmp
    ls -l /tmp/XYZ
    stat -c 'type=%F owner=%U uid=%u group=%G mode=%a inode=%i size=%s' /tmp/XYZ
    mkdir -m 700 "$dest" || { set +x; return 1; }
    cp -p logs/task2b-20261003-052529-summary.txt logs/task2b-20261003-052529-last-output.txt "$dest/"
    stat -c '%n type=%F owner=%U uid=%u group=%G mode=%a inode=%i size=%s mtime=%y' \
        /tmp /tmp/XYZ > "$dest/original-metadata.txt"
    cp --preserve=timestamps /tmp/XYZ "$dest/XYZ-content.bin"
    sha256sum /tmp/XYZ "$dest/XYZ-content.bin"
    sha256sum logs/task2b-20261003-052529-*.txt
    head -n 4 "$dest/task2b-20261003-052529-summary.txt"
    tail -n 5 "$dest/task2b-20261003-052529-summary.txt"
    sha256sum /etc/passwd
    grep '^test:' /etc/passwd || printf 'No test record in /etc/passwd\n'
    set +x
    printf '\nOriginal log preserved verbatim. No terminal completion line.\n'
    printf 'Last recorded progress: 76000 attempts / 227s; final totals unknown.\n'
    printf 'File-exists error was reported by the user; its original terminal is closed.\n'
}
preserve_failure
unset -f preserve_failure
