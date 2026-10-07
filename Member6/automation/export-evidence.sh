#!/usr/bin/env bash
# Archive existing guest evidence/source only. No generated terminal/screenshots.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd -P)
source "$HERE/guest-guard.sh"
m6_require_guest
cd /home/seed/issd-member6/lab-files
m6_require_workspace
m6_no_attacker
cd ..
label=${1:?Supply a fresh export label, for example session-20261007-1}
[[ $label =~ ^[A-Za-z0-9_-]+$ ]] || exit 1
mkdir -p exports
archive="exports/member6-$label.tar.gz"
[[ ! -e $archive && ! -e $archive.sha256 ]] || {
    echo 'STOP: preserve the existing export; choose a new label.' >&2; exit 1;
}
for directory in evidence provenance lab-files/logs; do
    [[ -d $directory ]] || { echo "Missing $directory" >&2; exit 1; }
done
# Keep root's account backup and all shadow/credential files out of the export.
unexpected=$(find evidence provenance lab-files/logs -type f \( -iname '*shadow*' -o -name 'issd-member*-passwd.*' -o -name '*.key' -o -name '*.pem' \) -print)
[[ -z $unexpected ]] || { printf 'STOP: inspect excluded private files:\n%s\n' "$unexpected" >&2; exit 1; }
tar -czf "$archive" --exclude='*shadow*' --exclude='*.key' --exclude='*.pem' \
    lab-files/cow_attack.c lab-files/cow_control.c lab-files/build.sh \
    lab-files/run_trial.sh lab-files/SOURCE_SHA256SUMS lab-files/logs \
    automation evidence provenance
(cd exports && sha256sum "member6-$label.tar.gz" > "member6-$label.tar.gz.sha256")
printf 'Saved existing evidence: %s\n' "$HOME/issd-member6/$archive"
cat "$archive.sha256"
echo 'Copy the archive and checksum to the host before any snapshot rollback.'
