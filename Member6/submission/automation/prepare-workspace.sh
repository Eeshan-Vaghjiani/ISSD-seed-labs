#!/usr/bin/env bash
# Copy this pack from a read-only share/data CD to a NEW native guest workspace.
# This copies source; compilation is the separate documented bash build.sh step.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd -P)
PACK=$(cd "$HERE/.." && pwd -P)
source "$HERE/guest-guard.sh"
m6_require_guest
DEST=/home/seed/issd-member6
if [[ -e $DEST || -L $DEST ]]; then
    echo 'STOP: ~/issd-member6 already exists. Inspect/compare it instead of overwriting work.' >&2
    exit 1
fi
(cd "$PACK/lab-files" && sha256sum -c SOURCE_SHA256SUMS)
mkdir -m 700 "$DEST"
mkdir -m 700 "$DEST/lab-files" "$DEST/automation" "$DEST/reference" \
    "$DEST/evidence" "$DEST/provenance" "$DEST/evidence/logs" "$DEST/lab-files/logs"
for name in cow_attack.c cow_control.c build.sh run_trial.sh SOURCE_SHA256SUMS; do
    cp -- "$PACK/lab-files/$name" "$DEST/lab-files/$name"
done
cp -- "$PACK"/automation/*.sh "$PACK"/automation/*.py "$DEST/automation/"
cp -- "$PACK/reference/Dirty_COW.pdf" "$PACK/reference/Labsetup.zip" "$DEST/reference/"
cp -- "$PACK/README.md" "$PACK/START_TO_FINISH_GUIDE.md" \
    "$PACK/ARCH_HOST_SETUP.md" "$PACK/VM_SESSION_GUIDE.md" "$DEST/"
cp -- "$PACK/evidence/SCREENSHOT_CHECKLIST.md" "$PACK/evidence/CAPTURE_PLAN.md" "$DEST/evidence/"
cd "$DEST/lab-files"
m6_require_workspace
sha256sum -c SOURCE_SHA256SUMS
if LC_ALL=C grep -n $'\r' -- *.c *.sh; then
    echo 'STOP: CR characters found. Inspect transfer before normalizing/rechecking source.' >&2
    exit 1
fi
bash -n build.sh
bash -n run_trial.sh
command -v gcc
pwd
df -T .
ls -l
echo 'Source copied and checksum-verified on native guest storage. Build separately with bash build.sh.'
