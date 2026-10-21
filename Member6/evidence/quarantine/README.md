# Quarantine — 21 Oct 2026

Two files overwrote tracked originals on 21 Oct 2026 and were moved here after
the originals were restored byte-identical from git (sha256 verified against
`HEAD`).

## 2026-10-21-vm-boot-rehearsal-capture.webm

A 599.7 s VirtualBox screen recording of the VM display, produced by the
machine's own capture-at-boot setting (`<Recording enabled="true">` in
`ISSD-Member6-SEED12.vbox`), whose remembered target file is the evidence clip
`incoming/opus-fresh-20261008/M6-task2-login-screen0.webm` (from the 9 Oct
sessions). Boot was 13:45:29Z; the recording stopped at the configured
`maxTimeS="600"` cap (13:55:28Z). It shows the first minutes of the 21 Oct
rehearsal (login, environment check, transcript start, the failed demo-kit
copies, the share mount and both clean prep runs).

**Status: not evidence, not deliberately recorded.** Kept only as the user's
personal rehearsal reference. Recording-at-boot will be disabled (and the
target path blanked) at the next normal VM shutdown; until then avoid
rebooting the VM, and click the status-bar record dot if one appears.

## 2026-10-21-stray-four-slide-copy.pptx

A re-serialized copy of `Member6/group-slides/Member 6 slides only.pptx`
(same four slide titles, verified) that replaced the merged deck
`ISSD presentation (Member 6 added).pptx` at the repo root around 16:39 local
— almost certainly a file-manager drag/copy mix-up. The merged deck was
restored from git (35 slides, sha256-verified). Nothing authored was lost;
this duplicate is safe to delete.

## Rule going forward

Never drag, copy or save files from the host or VM file managers over anything
under `Member6/evidence/` or the root pptx. Evidence files must stay
byte-identical to the committed hashes; restores happen only via git.
