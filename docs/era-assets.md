# Era image assets

The 1996, 2001 and 2006 eras use images that contain text or period graphics (buttons, tabs, pixel headings, the hit counter, the 2006 logo, the 1996 badges). `scripts/era-assets.py` draws them from the site's data and writes them to `assets/eras/<year>/`. The output is committed, so the Jekyll build never runs the script and doesn't need Pillow.

## Run it

```bash
pip install pillow pyyaml
python3 scripts/era-assets.py
```

Options:

- `--only shared | 1996 | 2001 | 2006 | badges | thumbs` draws one group (repeatable). `shared` is the square headshot every older era uses. `1996` includes the badges and the case-study thumbnails; `2001` includes the mobile tabs and header.
- `--out DIR` writes somewhere else (each era gets its own subfolder). Default: `assets/eras`.
- `--fonts DIR` uses another folder with `LiberationSans-Bold.ttf` and `LiberationMono-Bold.ttf`. Default: `scripts/fonts/`, which holds copies of both (SIL Open Font License; the license text is beside them).

Run it from anywhere; paths are relative to the repo. After a run, commit whatever changed in `assets/eras/`.

## Changing a label

Edit the YAML, re-run the script, commit the YAML and the images together. Alt text for these images comes from the same YAML field as the label, so the page and the picture stay in step.

| Image text | Where it comes from |
|---|---|
| Button and tab labels (About, Work, Résumé, Contact) | `_data/navigation.yml`, `name` |
| "Download résumé (PDF)", "Download portfolio (PDF)" | `_data/site.yml`, `resume.button` and `portfolio.button` |
| "Oren Kravetz" (2001 name, 2006 logo) | `_data/site.yml`, `name` |
| 2001 heading "Experienced Designer and Manager" | `_data/about.yml`, `heading` |
| "Case studies", "More work", "Clients", "Get in touch" | `_data/site.yml`, `labels` |
| 2001 "Loading", "Skip intro >>", "Replay intro"; 2006 "beta" | `_data/eras.yml`, that era's `ui` |
| Hit counter "0001996" | `_data/eras.yml`, the 1996 `label`, padded to seven digits |
| Badge file names and alt text | `_data/eras.yml`, the 1996 `badges` |
| Square headshot for the older eras (`assets/eras/headshot-square.jpg`, 256 × 256) | `_data/site.yml`, `headshot.square_original`: Oren's original square photo in `assets/incoming/`, scaled down |
| 1996 case-study thumbnails (120 × 90) | `_data/casestudies.yml`: each published study's `card_image`, scaled down; alt text is its `image_alt` |

The 2001 pixel font has no accents, so those images use plain letters and capitals ("Résumé" becomes "RESUME"). The script stops with an error if a label contains a character that can't be reduced to plain ASCII.

`index.html` and `contact.html` still hard-code the "labels" headings, so if you change one, change it in both places until the templates read from `site.yml`.

## The 1996 badges

The source is one image with both badges stacked on a white background (`badge_source` in `_data/eras.yml`, in `assets/incoming/`, which is never published). The script:

1. Finds the contiguous bands of non-white rows, one per badge. It stops with an error if the count doesn't match the `badges` list.
2. Flood-fills the white outside each badge, starting from its corners, and makes it transparent.
3. Resizes each to 176 × 62 (shown at 88 × 31) and writes `96-badge-<id>.png`.

To use a new source image, change `badge_source` and run `python3 scripts/era-assets.py --only badges`.

## Reproducibility

The output was checked against the original canvas scripts (`assets/incoming/era-assets-gen.py`, `era-assets-gen-mobile-tabs.py`, `era-badges.py`): all 66 images they make match pixel for pixel when drawn with the same Liberation fonts and Pillow 12.3.0. The case-study thumbnails were added later and have no canvas original. A different Pillow version may change GIF palettes or PNG bytes slightly, so re-run it only when a label or design changes, not as a routine step.
