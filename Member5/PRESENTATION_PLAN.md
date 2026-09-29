# Member 5 — presentation and live-demo plan

**Suggested 5–7 minute segment; confirm the group's actual allocation.** Complete the real lab runs and insert your own evidence before presenting. This is a slide/content plan, not a claim that the demonstrations have already been performed.

## Slide 1 — what is the vulnerability? (about 40 seconds)

**Title:** Race condition: the checked file is not necessarily the used file

Show the four-step timeline from the guide. Keep text short:

* Check: `/tmp/XYZ -> /dev/null`.
* Attacker changes the symlink.
* Use: `/tmp/XYZ -> /etc/passwd`.
* Root-effective victim appends the input.

**Say:** “A race condition means the result depends on timing. Here the program checks one target and later opens another target through the same filename. This is called time of check to time of use, or TOCTOU.”

## Slide 2 — environment and vulnerable code (about 45 seconds)

Show actual VM details and the few `access()`/`fopen()` lines. Insert S02–S04 selectively, not whole unreadable desktop screenshots.

**Say:** “I used [INSERT actual SEED OS/kernel]. The program is deliberately root-owned and Set-UID. I run it as the ordinary seed user. The check uses the real user identity, while the open has effective root privileges. The attack relies on the name being changed between these two calls.”

Explain that the lab temporarily disables specified Ubuntu protections for the attack experiment and later tests them again.

## Slide 3 — live slow-motion demonstration (about 90 seconds)

**Label visibly:** “Task 2.A — artificial 10-second delay for explanation.”

Before your slot, verify that both terminals are in `~/issd-member5/lab-files`, baseline has no `test` entry, binaries are built/Set-UID, no attackers are running and both lab controls are 0. Do not restore the baseline while processes are running. Use the guide's reset steps after each rehearsal.

**Terminal A, before starting the victim:**

```bash
ln -s /dev/null /tmp/XYZ
ls -l /tmp/XYZ
```

**Terminal B:**

```bash
id
./vulp_slow < input.txt
```

**Terminal A, after “Check passed” and within 10 seconds:**

```bash
ln -sfn /etc/passwd /tmp/XYZ
ls -l /tmp/XYZ
```

**Terminal B, after the program returns:**

```bash
grep '^test:' /etc/passwd
su - test
id
```

At the password prompt use the behaviour validated in Task 1. Explain that **`uid=0`** is the evidence. Exit the root shell after showing it.

**Say:** “The user cannot directly write the target. The privileged application performs the write on their behalf after checking the wrong object. I added a delay here so you can see the timing; the next result is from the genuine no-delay run.”

If the switch misses the window, say so and show your saved S06/S07 evidence. Do not use `sudo` to fake the account-creation result.

## Slide 4 — actual no-delay attack and improvement (about 60 seconds)

Show your S09 and S11 results and this small table:

| Method | My attempts / duration | My result |
|---|---|---|
| Naive unlink/create | [INSERT] | [INSERT] |
| Atomic `RENAME_EXCHANGE` | [INSERT] | [INSERT] |

**Say:** “The genuine attack runs the link-changing process and the victim concurrently with no artificial sleep. The naive attacker can leave a missing pathname, allowing the victim to create a root-owned file. The sticky bit then prevents the attacker removing it. Atomic exchange removes that particular gap.”

If you did not observe the sticky-bit failure, identify it as the documented explanation, not a witnessed result. Avoid claiming that one faster trial proves a general performance advantage.

## Slide 5 — countermeasures and evidence (about 60 seconds)

Show S12 and S13, plus your actual trial summaries:

* Least privilege: open/write as the ordinary user.
* OS defence: `fs.protected_symlinks=1` blocks this cross-owner traversal in sticky world-writable `/tmp`.
* Secure design: descriptor-based operations, safe temporary-file creation, restricted directories and security-relevant atomic operations.

**Say:** “For the first defence I changed the program and left OS protections off. For the second I used the original vulnerable program and turned on the symlink defence. This separates the two experiments. In my runs, [INSERT measured outcomes]. A timeout alone is not proof, so I also explain the mechanism that prevents the write.”

## Slide 6 — impact and takeaway (about 30 seconds)

**Takeaway:** “Do not check an attacker-controlled name and later use it with more privilege.”

**Say:** “A UID-0 entry can undermine the account database used by authentication. The account name itself is not special; UID 0 is what gives root access. Correct privilege handling and secure file operations are needed alongside OS protection.”

Transition to Member 6 if their segment follows: “This race is in application-level file handling. The next lab examines a different race in the kernel's copy-on-write mechanism.”

## Questions to practise

**Why not just protect `/etc/passwd` with permissions?** It is already protected from the ordinary user. The root-effective victim performs the write, so the flaw lies in the privileged program.

**Does a symlink give root access by itself?** No. It changes name resolution; a vulnerable privileged operation supplies the forbidden access.

**Why is `access()` insufficient?** It checks a mutable pathname at one instant and does not bind a later open to that same object.

**Why use `/dev/null`?** The ordinary-user permission check can pass, and any unsuccessful ordinary write to that target is discarded.

**Why does `whoami` show root after `su - test`?** Both entries map to UID 0; username lookup may choose root. `id` establishes the privilege.

**Did you use `sudo` to gain root?** Only for installing the intentionally privileged victim, the official manual validation and controlled reset. The real attack processes run as `seed`; show the commands and identity evidence.

**Why keep `/tmp`'s sticky bit enabled?** It is normal system behaviour and explains why the naive attack can get stuck on a root-owned file.

**Does atomic exchange fix the victim?** No; it fixes the attacker's unlink/create gap. The victim still checks and uses separately.

**Is the slow demo the real attack?** No; it is official Task 2.A. The no-delay experiments are Tasks 2.B and 2.C, shown with separately collected evidence.

**Does this prove all races are fixed by symlink protection?** No. The protection depends on directory and ownership conditions and does not solve general TOCTOU problems.

**What does this have to do with AI or authentication?** The direct result is a local threat to account integrity. Automation could make repeated trials easier, but AI is not required for this flaw and the lab does not demonstrate an AI-specific attack.

## Rehearsal checklist

* [ ] Confirm personal time allowance and slide numbering with the group.
* [ ] Replace all measurements and screenshots with your real results.
* [ ] Verify reset state, input file, Set-UID and control settings before the demo.
* [ ] Put the link-switch command in view before starting the 10-second window.
* [ ] Increase font size and silence unrelated desktop notifications.
* [ ] Keep saved real-attack screenshots/logs available outside the VM.
* [ ] Practise explaining each command rather than reading it without context.
* [ ] Exit root, stop processes and clean up after rehearsal/presentation.
