# TOC Edge Cases & Fixes

- **Headings without hashes**: TOC generation looks for `#`-prefixed headings. If a doc uses plain uppercase lines (e.g., `PART 1 PRELIMINARY`), prepend `## ` before running conversion or post-fix in the `.md`.
- **Duplicate headings**: Slugs get `-1`, `-2` suffixes. If anchors feel noisy, adjust heading text slightly (e.g., add the section number).
- **Too few headings**: TOC inserts only when ≥3 headings; force with `--toc`.
- **Short docs**: Auto-TOC suppressed when line count < threshold; lower via `--toc-threshold 60`.
