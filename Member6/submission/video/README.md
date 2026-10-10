# Genuine recorded Task 2 fallback

Open **TASK2_FALLBACK.mp4** on the host. It is a short, explicitly labelled presentation edit of the real **9 October 2026** VM recordings. Use it as recorded evidence, not as the result of a new classroom attempt.

## Sequence and edit boundaries

1. Three-second presentation title card.
2. **0–22 seconds** from `originals/M6-task2-recorded-screen0.webm`: seed identity, original charlie record, the actual bounded `fresh-t2-01` invocation and completed UID-only change.
3. Three-second transition card stating that authentication waiting is omitted.
4. **268–304.2 seconds** from `originals/M6-task2-login-screen0.webm`: the already-authenticated fresh non-sudo session; both earlier `su` attempts and the initial failure remain visible; actual `id`, `id -u`, `whoami`, proof PID, exit and return to seed are recorded.
5. Three-second closing card summarizing **separately evidenced** exact restoration and cleanup in S11/S13. Restoration itself is not footage in these source recordings.

The actual encoded fallback is **66.6 seconds**. The requested source intervals plus cards nominally total about 67 seconds; frame timing/encoding determines the final duration. `VIDEO_MANIFEST.json` records the actual encoded duration, hashes, full commands, source intervals and successful decode check. The card graphics are ordinary presentation graphics, not experimental terminal output. Native guest frames are transcoded to H.264 for playback; no terminal text is redrawn or overlaid.

## Uncut originals

* `originals/M6-task2-recorded-screen0.webm` — **130.065 seconds**, original native trial recording.
* `originals/M6-task2-login-screen0.webm` — **313.096 seconds**, original native login recording, including waiting and the authentication retry.

These copies match the fresh original files and hashes. Both original recordings passed full sequential decoding. Initial random-seek frame extraction produced a VP8 error near the end; sequential decoding resolved the derivative extraction, with the issue and real diagnostic frames retained in the fresh provenance. The original videos were not altered.

## What to say

“This is recorded evidence from 9 October. The sole ordinary-seed trial changed only charlie's four-character UID field. The first authentication failed; its cause is unknown. The second non-sudo login gave numeric UID 0. We exited that shell, restored the entire normal file, and verified a new UID-1001 login and cleanup.”

The recorded **0 integer elapsed seconds** belongs to the attack wrapper, not to this video's playback duration. No finer race runtime or kernel-level attempt count was measured. Use `MAIN_PRESENTATION` slide 5 or backup slides 8/9 for the shorter static-evidence route.
