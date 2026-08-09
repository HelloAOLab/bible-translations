# AAB working notes

The Accessible Ancients Bible (AAB), a public-domain translation derived from the BSB. 66 USX files in this folder, one per book.

**Read before changing anything:**
- `accessible-ancients-bible-translation-brief.md` — the governing document: goals, rationale, every interpretive commitment, and the master change log. Current status line is the version of record.
- `aab-footnote-drafting-policy.md` — the 17 rules every footnote must follow.

## Tools (use these instead of writing inline scripts)

```
./tools/aab.py verse "ROM 3:25"    # text + footnotes
./tools/aab.py notes "LEV 16:10"   # footnotes only
./tools/aab.py find "soul"         # search running TEXT (footnotes excluded)
./tools/aab.py findnotes "kipper"  # search footnotes
./tools/aab.py count "purgation"   # per-book counts in running text
./tools/aab.py validate            # XML-validate all 66 books
./tools/aab.py replace GEN.usx "old" "new"   # safe 1-match replace + validate
```

`find` strips footnotes first, so it shows only what a reader sees. Run it before claiming a term is or is not used in the text; searching raw files conflates text with footnotes and gives false positives.

## Settled terminology (do not re-litigate)

| Term | AAB renders | Not |
|---|---|---|
| kipper (verb) | effect purgation | make atonement |
| chattat | purification offering | sin offering |
| asham | reparation offering | guilt offering |
| olah | ascension offering | burnt offering |
| shelamim | well-being offering | peace offering |
| kapporet | throne seat (object) | mercy seat, atonement cover |
| hilastērion, Rom 3:25 | place of purgation (function) | propitiation, atoning sacrifice |
| yom hakkippurim | Day of Purification | Day of Atonement |
| reach nichoach | soothing aroma | pleasing aroma |
| hasatan (OT, and NT intertexts) | the Accuser | Satan (valid; footnoted at each) |
| qedoshim / hagioi | holy ones | saints |
| nephesh / psychē | life, self, person | soul (kept only where it means the inner self) |
| sarx | flesh | sinful nature |
| pistis Christou (genitive) | the faithfulness of Christ | faith in Christ |
| raqia | firmament | expanse |
| Sheol / Hades / Gehenna / Tartarus | kept distinct | hell |

The act is "purgation"; the offering and the day are named by their result, "purification." Both are deliberate. See the note on Lev 1:4.

## House style

- **No em dashes** in footnotes or Brief prose (only inside a direct quotation).
- Footnotes explain to an ordinary reader at an eighth-grade level; every claim carries its Scripture reference.
- State the positive; do not deny a position to make a point.
- Name Satan plainly; never in-house shorthand.
- Ground claims in Scripture, not in later theologians.

## Private reference material

`reference/` is gitignored. Working papers (systematic theology, the family/corporate-person framework, Lamb of the Free notes) live there locally.

**Use them as background only.** They are never named, cited, or alluded to in a footnote, in the Brief, or in a commit message. Footnotes cite Scripture. This rule is absolute.

## Workflow

Branch `claude/update-bible-aab-3gE8Q`, PR into `main`. For every change:

1. Make the edit, then `./tools/aab.py validate`.
2. Update the Brief: bump the status line, add a verse-catalog entry, and add master-change-log rows.
3. Commit and push; open or update the PR.

Discuss substantive translation choices before applying them. Mechanical fixes (typos, XML, doc-sync of decisions already made) can be applied directly.
