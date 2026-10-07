#!/usr/bin/env bash
# HOST ACTION: create ONLY the separate Member 6 VM; no boot or privileged host commands.
# Run after extracting and checksum-verifying the official archive.
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")/.." && pwd -P)
VM=ISSD-Member6-SEED12
MEDIA="$HOME/VirtualBox VMs/ISSD-Member6-media"
DISK="$MEDIA/SEEDUbuntu12.04/SEEDUbuntu12.04.vmdk"
[[ $(uname -m) == x86_64 && $EUID != 0 ]] || exit 1
[[ -f $DISK ]] || { echo "Missing verified descriptor: $DISK" >&2; exit 1; }
if VBoxManage showvminfo "$VM" >/dev/null 2>&1; then
    echo 'This VM is already registered. Inspect it rather than overwriting its configuration.' >&2
    exit 1
fi
if [[ -e "$HOME/VirtualBox VMs/$VM" ]]; then
    echo 'Existing VM directory found; inspect it before creating anything.' >&2
    exit 1
fi
for number in $(seq -w 1 41); do
    [[ -f "$MEDIA/SEEDUbuntu12.04/SEEDUbuntu12.04-s0$number.vmdk" ]] || {
        echo "Missing split VMDK part $number" >&2; exit 1;
    }
done
mkdir -p "$ROOT/evidence/host" "$ROOT/evidence/incoming"
LOG="$ROOT/evidence/host/vm-setup-$(date -u +%Y%m%dT%H%M%SZ).log"
[[ ! -e $LOG ]] || exit 1
configure() {
    set -x
    VBoxManage createvm --name "$VM" --platform-architecture x86 --ostype Ubuntu12_LTS \
        --basefolder "$HOME/VirtualBox VMs" --register
    VBoxManage modifyvm "$VM" --memory 2048 --cpus 2 --ioapic on --x86-pae on \
        --x86-long-mode off --firmware bios --graphicscontroller vmsvga --vram 64 \
        --accelerate-3d off --boot1 disk --boot2 dvd --boot3 none --boot4 none \
        --nic1 nat --nic-type1 82540EM --cable-connected1 off \
        --clipboard-mode hosttoguest --drag-and-drop disabled --audio-enabled off \
        --usb-ohci off --usb-ehci off --usb-xhci off
    # The supplied descriptor declares lsilogic; preserve that disk-controller family.
    VBoxManage storagectl "$VM" --name M6-SCSI --add scsi --controller LsiLogic --bootable on
    VBoxManage storageattach "$VM" --storagectl M6-SCSI --port 0 --device 0 \
        --type hdd --medium "$DISK"
    VBoxManage storagectl "$VM" --name M6-IDE --add ide --controller PIIX4
    VBoxManage storageattach "$VM" --storagectl M6-IDE --port 0 --device 0 \
        --type dvddrive --medium emptydrive
    VBoxManage sharedfolder add "$VM" --name M6pack --hostpath "$ROOT" --readonly
    VBoxManage sharedfolder add "$VM" --name M6export --hostpath "$ROOT/evidence/incoming"
    VBoxManage snapshot "$VM" take M6-clean-SEED12 \
        --description 'Verified official SEED12 disk; powered off before first boot, lab transfer, target creation or account changes.'
    VBoxManage showvminfo "$VM" --machinereadable
    VBoxManage snapshot "$VM" list --machinereadable
}
configure 2>&1 | tee "$LOG"
printf 'Host configuration log: %s\n' "$LOG"
