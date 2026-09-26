# Swole Streets website

Static, dependency-free website for the workout tracker and solo game. Existing page URLs (`index.html`, `faq.html`, `privacy.html`, `terms.html`) are preserved. No analytics, cookies, remote fonts, or JavaScript are required.

## Preview

From this directory:

```sh
python3 -m http.server 8769 --bind 127.0.0.1
```

Open `http://127.0.0.1:8769`. This is a local preview, not a deployment. Publishing requires a separately authorized commit/push to this website's remote; the iOS repository is separate.

## Content and legal documents

The homepage and FAQs focus on free manual workout logging and solo play: entering and editing workouts, reusable templates, units, Calendar/Trends, five game upgrade categories, up to three spendable points per day, one automatically saved solo game, earned coins, and local records. They do not promote unavailable modes or discuss retired AI entry. The three-point game reward allowance does not cap workout logging.

Goal creation is now free without a daily or lifetime cap. Its subscription check, paywall, rate-limit banner, and counter increments have been removed from the app; old saved counter keys are left intact and ignored. Other subscription infrastructure and disclosures are outside that focused change. The three-point game reward allowance is unchanged.

`legal-content.json` is exported from `../Todd/Todd/LegalContent.swift`. The current app still calls itself Todd in these documents, so those words, the effective date, and the multiplayer disclosures are deliberately preserved verbatim. A note outside the document explains the new public name and multiplayer's current availability. Future legal rebranding should begin in the app's source, followed by a website sync.

On a Mac with Xcode's Swift toolchain:

```sh
python3 scripts/sync_legal.py --app ../Todd
python3 scripts/sync_legal.py --app ../Todd --check
python3 scripts/check_site.py
```

The sync command only reads the app repository. It updates the exported JSON, document body regions, and effective dates. `--check` exits unsuccessfully if either website document has drifted from the app. The portable site check verifies links, anchors, image dimensions, accessible image descriptions, and legal text against the export.

## Visual sources

- Colors and typography: `Todd/RetroDesign.swift`.
- Fonts: unchanged copies of the app's bundled Press Start 2P and VT323, with their SIL Open Font License files in `assets/fonts/`.
- `assets/workout-editor.png`: actual `ManualWorkoutEditView` with sample workout data; it uses the shared workout field editor.
- `assets/workout-history.png`: actual `WorkoutsView` with an in-memory sample profile and workout.
- `assets/story-game.png`: actual `GameArenaView` rendering the City story level.

These are original app renderings captured on an iOS Simulator, not AI-generated substitutes or screenshots of a user's real workout records. The pictures retain the currently rendered app labels. Their clickable links open the full-size original images. The site uses shared styles in `styles.css`; navigation and FAQ disclosures work without JavaScript.

Download buttons and the App Store Smart App Banner are intentionally omitted for now. Add a verified download destination only when the owner is ready to offer one.
