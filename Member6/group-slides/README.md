# Member 6 — group-presentation slides (Dirty COW)

Your four slides for the shared class deck, in the group's own style (dark
theme, Russo One / Roboto, cyan `29C7FE` / pink `ED218F`, same card layouts as
Member 5's Race-Condition slides so the deck flows seamlessly).

## Where to use what

* **`../../ISSD presentation (Member 6 added).pptx`** — the group deck, ready to
  present/upload: their slides 1–31 + your slides **32–35**; the 20 leftover
  template slides (32–51 in the original) were deleted as the group's
  instruction required. Use this file.
* **`Member 6 slides only.pptx`** — just the four slides, same theme (backup,
  or for copy-pasting into another copy of the group deck).
* **`Member 6 slides only.pdf`** — quick-view PDF of the four slides.

## The four slides

1. *Dirty COW: the kernel's copy-on-write race* — concept + 4-line pseudo-code
   (read-only private map → `/proc/self/mem` write → `MADV_DONTNEED`, repeat).
2. *Live demonstration* — the three classroom steps (denial, normal COW, race).
3. *Result: file changed, then uid 0* — two strips cropped from the genuine
   9 Oct 2026 framebuffer captures (`assets/`, with exact provenance in
   `../evidence/incoming/opus-fresh-20261008/`).
4. *Countermeasures* — patch, update, limit + monitor, written from the report.

Each slide has short speaker notes.

## Rebuild (host-side)

```bash
/tmp/opencode/member6-docs-venv/bin/python Member6/group-slides/build_group_slides.py
```

The script reads the group deck at the repo root, crops the two screenshot
strips from the evidence PNGs, appends the slides, deletes the template slides,
and rewrites both packages (zip-deduped).python-pptx / Pillow come from
`../tools/requirements-docs.txt`.
