# Member 6 — document and evidence verification

**Fresh experiments: 9 October 2026. Final package review: 10 October 2026.** The technical work and the report/deck/support materials are complete. The machine-readable results are in [`provenance/SUBMISSION_VERIFICATION.json`](provenance/SUBMISSION_VERIFICATION.json); the content assessment is in [READINESS_REVIEW.md](READINESS_REVIEW.md).

## Verified artifacts

| Artifact | PDF pages / slides | Embedded images |
|---|---:|---:|
| REPORT | 16 | 19 captioned figures |
| MAIN_PRESENTATION | 10 slides: six main, four backup | Genuine evidence excerpts; notes on every slide |
| LIVE_DEMO | 3 | — |
| LIVE_COMMANDS | 1 | — |
| LIVE_PREPARATION | 3 | — |
| SLIDE_NOTES | 3 | — |
| TASK2_FALLBACK.mp4 | 66.6 seconds | Native recorded frames and explicitly separate title cards |

## Completed checks

* **21 selected original PNGs** match the fresh capture files and selection hashes. Eighteen are genuine guest framebuffers, three are user-supplied host views. Guest capture sidecars identify the exact VM UUID.
* **20 figure derivatives** match the original/derivative hashes and exact decoded pixels of the rectangles in `figures/CROP_MANIFEST.json`. No terminal text was recreated. Nineteen figures are embedded in the report.
* All four supplied C/build/trial files match `SOURCE_SHA256SUMS` and the verified final guest archive. The supplied source was preserved with LF line endings.
* All packaged trial/control/restoration logs match the exported originals. Task 1's complete 19-byte replacement and Task 2's complete 2040-byte UID-field-only replacement agree with their hashes, metadata and live-verification logs. The original and restored account files are byte-identical.
* Both closed raw transcripts are retained. The authentication failure, successful non-sudo UID-0 proof, proof PID 3392, new ordinary UID-1001 login and cleanup are consistent with the image reviews and guest export checks.
* The final guest archive's 46 file entries, checksum, original source hashes, closed transcript hash, restored account file and cleanup log were checked on the host. The protected root-held backup stayed in the guest.
* Packaged Python helpers parse; packaged shell helpers pass `bash -n`. Host-only build/media/verification tools are syntax-checked separately from guest execution.
* DOCX files pass ZIP integrity checks and reopen successfully. Every paragraph and table cell agrees with exported PDF text after whitespace/soft-hyphen normalization; both PDF stream and geometric reading order are considered for font-fallback glyphs.
* The finished Markdown sources contain no unfilled experimental-result placeholders. All figure references exist, and their count agrees with the DOCX image count.
* PDF extracted words stay within page bounds. The PPTX reopens with ten slides, notes on each slide, matching per-slide PDF text and all shapes within slide bounds.
* Both original WebM recordings passed full sequential decoding. The H.264 fallback passed full decoding, and source-copy hashes, edit intervals, cards and actual duration are recorded in `video/VIDEO_MANIFEST.json`.
* The report, deck, command sheet, preparation guide and notes were visually reviewed through rendered pages/contact sheets. Actual encoded video frames were inspected at the cards, trial result, authentication proof and session exit. The final slide-six spacing and preparation title were checked in a combined preview. The live guide was reflowed to three pages to remove a nearly empty fourth page.

## Retained qualifications

1. **S06 and S09 show completed trials.** The original S06 checklist filename contains “running”; captions state when it was actually captured.
2. **One authentication attempt failed.** Its cause is unknown, and both the failure and successful non-sudo retry remain in S10, the raw transcript and original recording.
3. **The first transcript lacked a completion footer.** An initial footer assertion failed. Closure was established from recorder/process exit and matching native/copied/archive bytes; no footer was inserted.
4. **The final explicit output-share unmount failed with password-required.** The input share was successfully unmounted; after verified export, normal guest shutdown closed remaining mounts. The final VM state was rechecked as `poweroff`, with the cable disconnected.
5. **Initial random-seek video-frame extraction emitted VP8 errors.** Full sequential decoding passed, and output-side seeking from a sequential decode produced the reviewed derivatives. The original media and diagnostic record were retained.
6. **An initial PDF-text audit flagged arrow headings.** PDF font fallback had placed arrows in separate text objects. Checking geometric reading order verified the intact headings without dropping glyphs or altering document text.
7. **S12 is not performed; discussion only.** No patched-guest outcome, high-resolution race runtime or kernel attempt count is inferred.

## Build and export provenance

The document sources are the completed Markdown files in this directory. `Member6/tools/build_submission.py` uses python-docx, python-pptx and Pillow, with Member 5's existing deck primitives for consistent visual style. LibreOffice on Arch exported the DOCX/PPTX files to PDF; export commands/results are in `provenance/PDF_EXPORT.json` and `provenance/PDF_EXPORT_LIVE_DEMO_FINAL.json`.

The media builder uses the original native VirtualBox recordings and ffmpeg. Title cards explicitly identify recorded excerpts and omitted waiting time. The card summarizing restoration refers to S11/S13; it is not represented as video of restoration.

## Reproduce the package checks — HOST

Run from the repository root with the existing document environment:

```bash
/tmp/opencode/member6-docs-venv/bin/python Member6/tools/verify_submission.py
(cd Member6/submission && sha256sum -c SHA256SUMS)
```

The first command is read-only by default. `--record` intentionally refreshes the machine-readable audit after a new build; `--render` writes page previews under `/tmp/opencode`. Refresh the checksum inventory after changing generated files or audit records.

If a reboot has cleared the temporary environment, recreate only the host document dependencies:

```bash
python -m venv /tmp/opencode/member6-docs-venv
/tmp/opencode/member6-docs-venv/bin/python -m pip install -r Member6/tools/requirements-docs.txt
```

The original source artifacts and Member 5 shared deck builder must remain available in this repository for a rebuild. The existing finished PDF/DOCX/PPTX/MP4 files can be opened directly without Python. `SHA256SUMS` inventories the finished submission tree, excluding the inventory itself.

## Remaining delivery checks

The package has been checked on the local host. Actual spoken timing, projector legibility, the course's identity/deadline/format requirements and the final upload remain user actions. Follow `LIVE_PREPARATION.md`; distinguish the new live dummy attempt from the recorded 9 October results and clean up after rehearsal.
