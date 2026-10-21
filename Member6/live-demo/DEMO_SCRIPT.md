# Member 6 — live demo cheat-sheet

**Rehearsed end-to-end in the VM on 21 Oct 2026 — every step below ran exactly
as written (prep even ran twice, both clean). Follow it top to bottom on the
day and nothing should surprise you.**

**Your part in 3 sentences:** you show that seed — an ordinary user, no sudo —
can change a root-owned file `/zzz` because of a kernel bug (Dirty COW,
CVE-2016-5195). Live, you do that on the dummy file (Task 1); Task 2 (charlie
becoming root) is shown from the recorded evidence; you finish with
restoration and countermeasures. Kit: `demo-prep.sh`, `demo-live.txt`,
`demo-cleanup.sh`. Formal version: `../submission/LIVE_DEMO.md`.

---

## 0. Start the VM

VirtualBox → **ISSD-Member6-SEED12** → Start. Log in as **seed** (type the
password yourself — never paste it). Open a terminal: **Ctrl+Alt+T**.

> **Watch the record dot (learned the hard way on 21 Oct).** This VM still has
> VirtualBox screen capture enabled at boot: it records the first **10
> minutes** and saves them *straight into an evidence file* in the repo
> (overwriting it — we restored the original from git and will disable the
> setting at the next normal shutdown). Until then: if a record dot shows in
> the VM window's status bar, click it to stop; do **not** reboot the VM
> mid-session; and never drag or copy files over anything under
> `Member6/evidence/` in the file manager — one drag replaced the deck once
> already today.

## 1. Check the lab is intact (paste, one line)

```bash
cd ~/issd-member6/lab-files && bash ../automation/check-environment.sh && sha256sum -c SOURCE_SHA256SUMS
```

Expected tail: *"Prescribed guest identity/release/kernel/architecture checks
passed"* and four `OK` lines (`build.sh`, `cow_attack.c`, `cow_control.c`,
`run_trial.sh`). **Stop if anything says FAILED.**

## 2. Start the recording shell (paste, one line)

```bash
LOG="../evidence/logs/demo-$(date -u +%Y%m%dT%H%M%SZ)-$$.typescript"; script -q -f "$LOG"
```

You get a new prompt — from here on everything you type is saved to an evidence
file. That is the point; do not exit this shell until the cleanup has run.

## 3. Get the demo kit (only needed once per VM start — fresh boot = not mounted)

Paste this block, then type the **VM sudo password** when asked (nothing shows
while typing; if it says *"Sorry, try again"*, just type it again — that
happened in rehearsal and cost nothing):

```bash
mount | grep -q m6-transfer && sudo umount ~/m6-transfer
mkdir -p ~/m6-transfer
sudo mount -t vboxsf M6pack ~/m6-transfer
ls ~/m6-transfer/live-demo
cp ~/m6-transfer/live-demo/demo-prep.sh ~/demo-prep.sh
cp ~/m6-transfer/live-demo/demo-cleanup.sh ~/demo-cleanup.sh
```

`ls` must show all four files (`DEMO_SCRIPT.md  demo-cleanup.sh  demo-live.txt
demo-prep.sh`). Already copied in a previous round? Skip this step.

*If the mount fails (e.g. "wrong fs type"):* clipboard route — open the script
on the host, Ctrl+A, Ctrl+C, click into the VM terminal, right-click → Paste.

## 4. Prep the demo file (once per round)

```bash
source ~/demo-prep.sh
```

Expected output, in order:

* `No matching process: cow_attack` / `No supplied trial wrapper is running` /
  `No matching process: su` — nothing from an earlier run is alive
* `/etc/passwd: OK` — the account file is untouched
* `uid=1001(charlie) ...` — charlie is still a normal user
* `/zzz: OK` — the root-owned demo file is created with the exact original bytes
* `RUN=presentation-dummy-...` and `== PREP DONE — ...` — ready

Asked for the sudo password once (the file creation step). **Leave this
terminal open** — `RUN` and the recording live here. Ran it twice by accident?
Harmless: it rewrites `/zzz` and takes a fresh label; just continue with the
newest `RUN` shown.

## 5. During the presentation (slide "Live demonstration")

Type one command, pause, say the line, read the screen. Same lines are in
`demo-live.txt`.

| Type | Say | What's actually happening (if someone asks) |
| --- | --- | --- |
| `id` | "I'm seed — UID 1000, an ordinary user. No sudo here." | Your identity: uid 1000, not 0. |
| `ls -l /zzz` | "`/zzz` belongs to root, mode 644 — only root may write." | Owner root + 644 = group/others get read-only. |
| `cat /zzz` | "Content: `111111222222333333`." | The baseline bytes you're about to attack. |
| `echo 99999 > /zzz` | "A normal write — **Permission denied.** Protection works." | Kernel checks permission first: uid 1000 ≠ owner root → denied. This is Unix working correctly. |
| `./cow_control` | "Copy-on-write the normal way: the program asks for a *private* writable copy of the file. It writes stars into its own memory…" | Opens `/zzz` read-only, maps it `MAP_PRIVATE` (writable in memory only). Writes go to the private copy. |
| `cat /zzz` | "…but the file on disk still reads the digits. Nothing leaked." | The mapping's backing file is untouched — COW doing its job. |
| `sha256sum -c ../provenance/dummy-normal.sha256` | "Hash check: the file is bit-for-bit the original." | Independent proof the control changed nothing. |
| `bash run_trial.sh dummy 15 "$RUN"` | "Now the race. It stops itself the moment the file changes — capped at 15 seconds in class." | `cow_attack` re-maps `/zzz` read-only *private*, then hammers two things at once: a write to its **own memory** through `/proc/self/mem`, and `madvise(MADV_DONTNEED)` to throw the private pages away. The kernel sometimes ends up writing into the *page cache of the real file* — that's the bug. When `/zzz` changes (or 15 s pass), the wrapper stops it and logs everything. |
| `cat /zzz` | "The root file now reads `111111******333333` — six middle bytes rewritten by seed, no sudo." | Exactly 6 targeted bytes changed — not random corruption; the race wrote the attacker's bytes through the kernel. |
| `ls -l /zzz` | "Still root-owned, still mode 644 — the write never opened the file." | Owner/mode unchanged: proof the write bypassed file permissions entirely. |

**If the race doesn't win live** (kernel timing varies — it happens): don't
fumble. Say *"scheduling is different on the day — here is the recorded run
from 9 October"* and move to the Result slide. Then still run the cleanup — it
keeps the honest record either way.

## 6. Right after the demo (same terminal)

```bash
bash ~/demo-cleanup.sh
```

It: saves after-metadata, runs the trial verifier (`trial verifier exit code:
0` = the live result was accepted; anything else = honest "race didn't win",
kept in the logs), checks no attacker or `su` process is left, compares
`/etc/passwd` against the normal copy (prints nothing + "passwd: identical"),
removes `/zzz`, and runs the full cleanup checker. End with `== CLEANUP DONE`.

Then type **`exit`** to leave the recording shell. If anything unexpected
appears, stop and use `../submission/LIVE_DEMO.md` recovery — don't improvise.

## 7. Rehearse it again and again

Two loops, both proven:

* **Quick loop** (practise the race a few times): `source ~/demo-prep.sh` —
  it rewrites `/zzz` back to the digits and picks a fresh `RUN` — then redo
  section 5. Old rounds keep their own logs under `logs/`.
* **Full loop** (exact dress rehearsal, includes verifier): `bash
  ~/demo-cleanup.sh` → `source ~/demo-prep.sh` → section 5.

Run cleanup **once per round**, not repeatedly. Final round ends with: cleanup
→ `exit` (leaves the recording) → shut the VM down normally if the day is over.

## 8. Task 2 — recorded, not live

Back on the slides: **Result** shows charlie's UID `1001 → 0000` and the fresh
non-sudo login returning `uid 0` — say clearly: *"this part is recorded
evidence from 9 October, not live."* Evidence: screenshots `M6-S08 → M6-S11`
or `../submission/video/TASK2_FALLBACK.mp4`.

## 9. One-line answers for questions

* *"Why can seed write a root file?"* — It never writes the file. It writes its
  own memory while a kernel race corrupts the shared page — the bug is in the
  kernel's copy-on-write handling, fixed upstream in 2016.
* *"What are the stars?"* — The six middle bytes the attacker wrote; positions
  and owner/mode prove it was targeted, not corruption.
* *"Why an old Ubuntu?"* — The bug needs the unpatched kernel; 12.04 with
  3.5.0-37 is the SEED lab's deliberately vulnerable target.
* *"Is it dangerous today?"* — No: patch and stay updated; our VM keeps the old
  kernel only to demonstrate.

---

**Passwords:** typed inside the VM only, never pasted anywhere.
**Evidence:** transcript + `logs/` capture every round, including the failed
first attempts in rehearsal — that's by design, keep them.
