# Member 6 — preparation and verification status

Research/check date: **29 September 2026**.

## Completed during preparation

* Reviewed the lecturer's links and the PDF's Member 6 responsibilities.
* Read the official Dirty COW lab page, complete upstream task text and original `cow_attack.c`.
* Read the five-page historical SEED Ubuntu 12.04 VM manual: it identifies Ubuntu 12.04, original kernel 3.5.0-37-generic, seed/dees account and historical VM configuration.
* Confirmed the official page explicitly requires the old SEED 12.04 image despite the `Labs_20.04` URL.
* Checked Ubuntu's CVE-2016-5195 advisory, including package-specific fix versions and backport considerations.
* Consulted memory-mapping/discard documentation to distinguish normal COW, read-only pointers and the `/proc/self/mem` write path.
* Mapped both official tasks and every Member 6 division item to the guide, report, presentation and evidence checklist.
* Reviewed the C source for bounded mapping search, exact account-prefix matching, same-length UID replacement, address-width handling, checked setup calls and ordinary-user execution.
* Checked `build.sh` and `run_trial.sh` individually with `bash -n` using Git for Windows Bash; both passed.
* Generated and reopened all three Word documents using `python-docx`, with matching paragraph/table counts and closed Markdown code fences.

## Not executed here

* No SEED Ubuntu 12.04 guest was installed or booted by the preparation agent.
* No Linux GCC compilation or C runtime verification was performed here. The host's GCC targets Windows, which cannot validate Linux COW/mmap/proc semantics.
* No dummy-file exploitation, account overwrite, root login or patched-kernel comparison is claimed.
* The monitor's process stopping and exact exploit behaviour must be verified during the documented VM trials.
* Word documents have been library-reopened, not visually paginated in Microsoft Word. Check page breaks, image placement and long commands when preparing the final submission.

## Checks to complete during your run

1. Confirm actual image/kernel/architecture and build with Linux GCC.
2. Verify ordinary dummy writes are denied and normal private COW leaves the backing file unchanged.
3. Observe the exact Task 1 replacement, retain failed/partial attempts and unique run logs.
4. Verify charlie starts with a normal UID, back up after its creation, then test Task 2.
5. Validate only the intended UID field changes and a fresh non-sudo login has UID 0.
6. Restore normal UID, close privileged sessions and confirm no attacker process remains.
7. Label the patched comparison accurately as performed or discussion-only.

The public source links are research references. The old VM image itself was not downloaded or checksum-tested here; the guide instructs you to verify your download. Deadlines, report format and personal speaking time remain to be confirmed because they are absent from the supplied course material.
