# Official Dirty COW references

The host preparation copies these exact downloads here for offline transfer to the old guest:

* `Dirty_COW.pdf`: <https://seedsecuritylabs.org/Labs_20.04/Files/Dirty_COW/Dirty_COW.pdf>
* `Labsetup.zip`: <https://seedsecuritylabs.org/Labs_20.04/Files/Dirty_COW/Labsetup.zip>

Source/file hashes are recorded in `../evidence/host/transfer-20261007-final.json`; the earlier `transfer-20261007.json` preserves the initial bundle. `Labsetup.zip` is intentionally ignored by the repository's existing `.gitignore`; it is present locally and in the prepared data CD. For a fresh checkout, download it from the exact URL above before preparing transfer media.

Inside the VM, copy these files to `~/issd-member6/reference/` and unzip the original source **there**, on the native Linux filesystem. Read the original alongside the repository's `lab-files/cow_attack.c` adaptation. Their implementations are distinguishable; use the assigned repository adaptation for the experiments.

The historical [Ubuntu 12.04 VM manual](https://seedsecuritylabs.org/Labs_12.04/Ubuntu12_04_VM_Manual.pdf) identifies kernel `3.5.0-37-generic`; its original GFDL notice remains with the linked manual. The [SEED download page](https://seedsecuritylabs.org/labsetup.html) publishes the old image and its MD5.

Ubuntu advisory fallback consulted on 7 October 2026: <https://git.launchpad.net/ubuntu-cve-tracker/plain/retired/CVE-2016-5195>. The normal advisory web page returned HTTP 504 during this audit. The official tracker distinguishes the old `linux-lts-quantal` stream from the fixed 3.2/3.13 package families.

Dirty COW task/source pattern: **Copyright 2017 Wenliang Du / SEED Labs; CC BY-NC-SA 4.0**. Retain the original PDF notice and repository attribution.
