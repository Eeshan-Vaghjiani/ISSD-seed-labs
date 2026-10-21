# Member 6 — live demo cheat-sheet

**Your part in 3 sentences:** you show that seed — an ordinary user, no sudo —
can change a root-owned file `/zzz` because of a kernel bug (Dirty COW,
CVE-2016-5195). Live, you do it on the dummy file (Task 1); Task 2 (charlie
becoming root) is shown from the recorded evidence, and you end with
restoration + countermeasures. Copies: `demo-prep.sh`, `demo-live.txt`,
`demo-cleanup.sh`. The full formal version is `../submission/LIVE_DEMO.md`.

---

## 1. Before class (~3 min, inside the VM)

Start VirtualBox → **ISSD-Member6-SEED12**, log in as **seed** (type the
password yourself — never paste it), open a terminal (Ctrl+Alt+T).

**Paste 1 — checks the lab is intact** (stop if anything says FAILED):

```bash
cd ~/issd-member6/lab-files && bash ../automation/check-environment.sh && sha256sum -c SOURCE_SHA256SUMS
```

**Paste 2 — starts the recording shell.** You'll get a new prompt; from now on
everything you type is saved to an evidence file (that's the point):

```bash
LOG="../evidence/logs/demo-$(date -u +%Y%m%dT%H%M%SZ)-$$.typescript"; script -q -f "$LOG"
```

**Paste 3 — preps the demo.** Gets the script out of your recording shell… take
your pick:

- copy route: `cp ~/m6-transfer/live-demo/demo-prep.sh ~/ && source ~/demo-prep.sh`
- paste route: open the file on the host, select all, paste into the terminal

```bash
source ~/demo-prep.sh
```

It runs the guards, creates `/zzz` (asks for the **VM sudo password once — type
it**), and prints `RUN=…` and `PREP DONE`. If the share isn't mounted yet:
`mkdir -p ~/m6-transfer && sudo mount -t vboxsf M6pack ~/m6-transfer`
(the share is this repo's `Member6` folder).

Leave this terminal open and the VM running. Nothing else to do until your slot.

## 2. During (slide "Live demonstration")

Type these one at a time (same lines are in `demo-live.txt`), and say what each
shows:

| Type | Say |
| --- | --- |
| `id` <br> `ls -l /zzz` <br> `cat /zzz` | "I'm seed, UID 1000. `/zzz` belongs to root, mode 644 — and the content is digits." |
| `echo 99999 > /zzz` | "A normal write is refused — **Permission denied**. Protection works." |
| `./cow_control` <br> `cat /zzz` <br> `sha256sum -c ../provenance/dummy-normal.sha256` | "Copy-on-write the normal way: the program changes its **private copy** — memory shows stars — but the file on disk is untouched." |
| `bash run_trial.sh dummy 15 "$RUN"` | "Now the kernel race. It stops itself the moment the file changes — capped at 15 seconds in class." |
| `cat /zzz` <br> `ls -l /zzz` | "The root file now reads `111111******333333` — still root-owned, mode 644. Seed just rewrote it without sudo." |

**If the race doesn't win live** (kernel timing varies, it happens): don't
fumble. Say *"scheduling is different on the day — here is the recorded run
from 9 October"* and advance to the Result slide. Then still run the cleanup —
it keeps the honest record either way.

## 3. Right after (about 1 min, same terminal)

```bash
bash ~/demo-cleanup.sh
```

It saves the after-metadata, runs the trial verifier (exit 0 = verified result),
checks no attacker or `su` process is left, compares `/etc/passwd` against the
normal copy, removes `/zzz`, and runs the full cleanup checker. Then type
`exit` to leave the recording shell. If anything unexpected appears, stop and
use `../submission/LIVE_DEMO.md` recovery instead of improvising.

## 4. Then: show Task 2 from records, and finish

Back to the slides: **Result** (recorded Task 2 — charlie UID `1001 → 0000`,
fresh non-sudo login gives `uid 0`) and **Countermeasures** (patch, update,
limit, monitor). Task 2 evidence: screenshots `M6-S08 → M6-S11` or
`../submission/video/TASK2_FALLBACK.mp4`. Say clearly: *"this part is recorded
evidence from 9 October, not live."*

---

**Passwords:** always typed inside the VM, never pasted into files or chat.
**Evidence:** everything is timestamped and hashed in the transcript plus
`logs/` — that's why the recording shell comes first.
