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

The legal documents describe the current Swole Streets release: free manual tracking and solo play, local records and widgets, optional Supabase issue reports, automatic RevenueCat purchase-status checks, disabled real-money catalog purchases, and the handling of older subscriptions and records. They do not advertise multiplayer as available. Goal creation has no daily or lifetime cap; the three-point game reward allowance is separate.

`legal-content.json` is exported from `../Todd/Todd/LegalContent.swift`, the source of truth for both legal documents and their effective date. Start legal changes there, then sync and validate this site. Todd Labs remains the operator and support contact; Swole Streets is the app name. The app repository's `LEGAL_REVIEW.md` records the code audit, research, and operational follow-ups that legal copy alone cannot resolve.

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
