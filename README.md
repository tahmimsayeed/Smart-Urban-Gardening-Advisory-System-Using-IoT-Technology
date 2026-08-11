# Smart Urban Gardening Advisory System Using IoT Technology

Flask + Bootstrap 5 + SQLite implementation, built module by module per the
project's Phase 03 design (DFDs, Class Diagram, Use Cases, Sequence
Diagrams, Activity Diagrams, Deployment Diagram).

**All 8 modules are complete.** See "What's next" at the bottom of this
file for what's left before this is submission/demo-ready (mainly: train
the real ML model, since Disease Detection has been running in mock mode
this whole time).

## Module status

| # | Module | Status |
|---|---|---|
| 1 | Authentication (Register, Login, Logout) | ✅ Complete & tested |
| 2 | Plant Management (Add, Edit, Delete, View) | ✅ Complete & tested |
| 3 | Disease Detection (Upload, Predict, Confidence, Treatment, History) | ✅ Complete & tested |
| 4 | Weather Recommendation (Current Weather, 5-Day Forecast, Care Recommendation) | ✅ Complete & tested |
| 5 | IoT Sensor Module (Pair Sensor, Simulated Temp/Humidity/Soil Moisture) | ✅ Complete & tested |
| 6 | Alert Module (Threshold Alert, Disease Alert, Unread Count, History) | ✅ Complete & tested |
| 7 | Nursery Module (Add/Edit/Delete Product, Browse) | ✅ Complete & tested |
| 8 | Knowledge Base (Display plant care information) | ✅ Complete & tested |

The full database schema (all 10 tables) is now fully in use.

## Project structure

```
smart_garden/
├── app.py                  # application factory + entry point
├── config.py                # all settings, env-var overridable
├── extensions.py            # shared db / bcrypt / login_manager instances
├── models/                  # SQLAlchemy ORM models (one file per Class Diagram entity)
├── blueprints/
│   ├── auth/                 # Module 1: routes.py (register/login/logout)
│   ├── plants/                # Module 2: routes.py (add/edit/delete/view plant)
│   ├── disease/                # Module 3: routes.py (upload/diagnose/history)
│   ├── weather/                # Module 4: routes.py (weather + care recommendation)
│   ├── sensors/                # Module 5: routes.py (pair sensor + simulate readings)
│   ├── alerts/                 # Module 6: routes.py (thresholds, alert history, global feed)
│   ├── nursery/                # Module 7: routes.py (add/edit/delete product, browse)
│   └── knowledge_base/         # Module 8: routes.py (browse/search articles)
├── templates/
│   ├── base.html             # Bootstrap 5 navbar/layout, shared by every page
│   ├── auth/                 # register.html, login.html, placeholder_dashboard.html
│   ├── plants/                # dashboard.html, add.html, edit.html, view.html
│   ├── disease/                # diagnose.html, result.html, history.html
│   ├── weather/                # weather.html
│   ├── sensors/                # sensor.html
│   ├── alerts/                 # thresholds.html, plant_alerts.html, all_alerts.html
│   └── nursery/                 # my_products.html, add.html, edit.html, browse.html
│   └── knowledge_base/          # browse.html, article.html
├── static/
│   ├── css/custom.css        # small overrides on top of Bootstrap 5
│   └── js/main.js            # shared client-side behavior
├── utils/
│   ├── validators.py         # dependency-free input validation
│   ├── access_control.py     # shared ownership-based access control (Module 2+)
│   ├── ml_predictor.py       # loads plant_model.keras, runs inference, mock fallback
│   ├── treatment_tips.py     # disease label -> treatment recommendation lookup
│   ├── weather_service.py    # OpenWeatherMap calls + forecast caching
│   ├── recommendation_engine.py  # care recommendation rule engine
│   ├── sensor_simulator.py   # simulated moisture/temperature/humidity readings
│   ├── alert_engine.py       # threshold/disease alert triggering rule engine
│   └── seed_knowledge_base.py  # auto-seeded plant care/disease articles (Module 8)
├── uploads/                  # leaf images land here at runtime
├── ml_model/                 # put plant_model.keras + labels.json here (see Section 3)
├── .env                       # your local secrets (OPENWEATHER_API_KEY, etc.) -- not in git
└── .env.example                # template for .env
```

## Setup

```bash
cd smart_garden
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** -- you'll land on the login page. Click
Register to create a Gardener or Nursery Owner account.

## What's implemented and verified in Module 1

- **Register** (`GET/POST /auth/register`): name, email, password,
  confirm-password, account type (Gardener / Nursery Owner), and business
  name (required only for Nursery Owner). Full server-side validation
  (email format, password strength, matching passwords, duplicate email)
  with Bootstrap alert messages; re-renders the form with prior input on
  error (except passwords).
- **Login** (`GET/POST /auth/login`): email + password, bcrypt-checked
  against the stored hash, session created via Flask-Login, "keep me
  logged in" checkbox, redirects back to the originally-requested page via
  Flask-Login's `next` parameter.
- **Logout** (`GET /auth/logout`): clears the session, requires an active
  login to access (so hitting it while logged out just bounces to login).
- **Session protection**: any route decorated with `@login_required`
  (see `dashboard_redirect` for the pattern later modules should follow)
  redirects an anonymous visitor to `/auth/login?next=<original path>`.

All of the above was exercised end-to-end with curl + a cookie jar,
including the negative cases (wrong password, duplicate email, weak
password, missing business name for a Nursery Owner) -- every one behaved
as expected.

## What's implemented and verified in Module 2

- **Add Plant** (`GET/POST /plants/add`): name, type, and optional
  location, with server-side validation (required fields, length limits).
  Gardener-only -- a Nursery Owner is redirected with a friendly flash
  message rather than shown a raw error.
- **View Plant** (`GET /plants`, `GET /plants/<id>`): a card-grid dashboard
  of all the logged-in Gardener's plants, and a detail page per plant
  showing name/type/location and sensor-pairing status (placeholder text
  until the IoT Sensor Module exists).
- **Edit Plant** (`GET/POST /plants/<id>/edit`): pre-filled form, same
  validation as Add.
- **Delete Plant** (`POST /plants/<id>/delete`): Bootstrap modal
  confirmation dialog before submitting; POST-only route (no accidental
  deletion via a GET link/crawler).
- **Ownership-based access control** (Security NFR): every route checks
  that the requested plant's `ownerId` matches the logged-in user before
  allowing access -- verified with two separate Gardener accounts: Carol
  gets a 404 (not 403, so she can't even confirm the plant ID exists) when
  trying to view, edit, or delete a plant that belongs to Alice.
- **Session protection carried over from Module 1**: every `/plants/*`
  route requires an active login, redirecting anonymous visitors to
  `/auth/login?next=/plants` exactly like Module 1's pattern.

All of the above was exercised end-to-end with curl + cookie jars for
three separate accounts (two Gardeners + one Nursery Owner), including the
cross-account isolation checks -- every case behaved as expected.

## What's implemented and verified in Module 3

- **Upload Leaf Image** (`GET/POST /plants/<id>/diagnose`): file picker
  with a client-side image preview (small, self-contained JS -- no
  framework), server-side validation of file type/size.
- **Predict Disease + Confidence Score**: `utils/ml_predictor.py` loads
  `ml_model/plant_model.keras` (once you've trained it -- see Section 3
  below) and runs inference, returning a disease label and a confidence
  score shown as a progress bar on the result page.
- **Treatment Recommendation**: `utils/treatment_tips.py` maps each
  disease label to a specific treatment tip.
- **Save Disease History**: every diagnosis is saved to the
  `DiagnosisResult` table and viewable per-plant at
  `GET /plants/<id>/history`.
- **Mock mode**: since a trained model isn't available immediately, the
  module works end-to-end without one -- `ml_predictor.py` automatically
  falls back to a clearly-labeled mock prediction (a yellow warning banner
  says so on both the upload page and the result page) until you drop
  `plant_model.keras` + `labels.json` into `ml_model/`. No code changes
  needed when you do -- it's auto-detected.
- **Ownership-based access control carried over from Module 2**: verified
  that a second Gardener account gets a 404 trying to diagnose or view the
  disease history of a plant they don't own.
- **Uploaded images** are served through a login-protected `/uploads/<file>`
  route (not placed under `static/`, which Flask serves without auth) --
  verified 200 with a valid session, 302-to-login without one.

**Small refactor note**: the two ownership-check helper functions that
Module 2 defined privately inside `blueprints/plants/routes.py` were moved,
unchanged, into `utils/access_control.py` so Module 3 could reuse them
without importing another blueprint's private functions. This is a pure
relocation -- both functions are identical to their Module 2 originals,
just callable from anywhere now. A full regression test of Modules 1 and 2
was re-run after the move and everything still passes.

All of the above was exercised end-to-end with curl, including uploading a
real (generated) test image, an empty-file submission, an invalid file
type, and the cross-account isolation checks.

## Training the real model in Google Colab

1. Prepare your labeled dataset (organized into one sub-folder per disease
   class, per the project's dataset structure) and upload it to Google
   Drive.
2. In Colab, use transfer learning on MobileNetV2 (`weights="imagenet"`,
   frozen base + a small trained classification head -- do not train from
   scratch).
3. Export the trained model as `plant_model.keras`, and separately save
   the ordered list of class names as `labels.json` (a simple JSON array,
   e.g. `["Tomato_BacterialSpot", "Tomato_FreshLeaf", ...]` -- the index in
   this list must match the index of the model's output layer).
4. Download both files and place them directly inside this project's
   `ml_model/` folder (next to `.gitkeep`).
5. Restart the Flask app (`python app.py`). You should no longer see the
   mock-mode warning -- diagnoses will now come from your trained model.

If your dataset's class-folder names don't already match the
`<Vegetable>_<Condition>` format used in `utils/treatment_tips.py`
(e.g. `Tomato_BacterialSpot`), either rename them to match before
training, or extend `TREATMENT_TIPS` with your actual label strings so
every prediction gets a real treatment tip instead of the generic fallback.

## All 8 modules complete -- what's left

The app is feature-complete per the original spec. Before it's fully
submission/demo-ready:

1. **Train the real ML model** (Section 3 above) -- Disease Detection has
   been running in mock mode this whole time so every other module could
   be built and tested without waiting on it. This was always planned as
   the last step, done once, after every module was finished.
2. **Review the `.env` file** -- make sure `OPENWEATHER_API_KEY` is your
   own key before a final demo/submission, and consider changing
   `SECRET_KEY` to something random rather than the `dev-secret-change-me`
   default in `config.py`.
3. **Optional cleanup**: `templates/auth/placeholder_dashboard.html` is
   no longer linked from anywhere (both roles now land on a real
   dashboard) -- harmless to leave, or delete it if you want a tidier
   file tree.

## What's implemented and verified in Module 6

- **Set Threshold Alert Values** (`GET/POST /plants/<id>/thresholds`): a
  minimum soil-moisture percentage per plant, with validation (must be a
  number between 0-100).
- **Trigger Threshold Alert / Disease Alert**: `utils/alert_engine.py` is
  a direct implementation of the Phase 03 Activity Diagram -- an alert is
  only created if a threshold is configured AND breached (for sensor
  readings), or if the diagnosis label isn't "fresh/healthy" (for
  diagnoses). No threshold configured -> correctly no alert evaluation at
  all, verified directly.
- **Disclosed integration hooks** (the one deviation from "add a new
  module without touching old files," and an expected one -- the Activity
  Diagram defines alert triggering as *reacting to* a new sensor reading
  or diagnosis, so those two creation points had to call into the new
  alert engine):
  - `blueprints/sensors/routes.py`'s `simulate()` now calls
    `evaluate_sensor_reading()` right after saving a new `SensorReading`
    (3 lines added, no existing logic changed).
  - `blueprints/disease/routes.py`'s `diagnose()` now calls
    `evaluate_diagnosis()` right after saving a new `DiagnosisResult`
    (3 lines added, no existing logic changed).
  - Both hooks were verified with a full regression pass showing Modules
    3 and 5 still behave exactly as before, plus the new alert-creation
    behavior on top.
- **Unread Alert Count**: exposed globally via a Flask context processor
  in `app.py`, so it shows as a red badge next to "Alerts" in the navbar
  on *every* page, not just the alerts page itself -- verified by checking
  the badge count on the Plants Dashboard page after acknowledging an
  alert elsewhere, confirming it's a true global count, not a per-page one.
- **Alert History**: both a per-plant view (`/plants/<id>/alerts`) and a
  global feed across every plant (`/alerts`), each with "Mark as Read"
  buttons that flip status from unread to acknowledged and correctly
  decrement the unread count.
- **Ownership-based access control carried over**: verified a second
  Gardener account gets a 404 trying to view another Gardener's plant's
  alerts or set its threshold, and their own global feed correctly shows
  zero results for a plant they don't own.

All of the above was exercised end-to-end with curl, including a full
regression pass confirming Modules 1-5 still work correctly afterward.

## What's implemented and verified in Module 5

- **Register and Pair IoT Sensor Node** (`POST /plants/<id>/sensor/pair`):
  one sensor per plant (enforced both by the database's unique constraint
  on `Sensor.plantId` and a friendly check in the route); trying to pair a
  second sensor to an already-paired plant is rejected with a clear
  message instead of a database error.
- **Simulated Temperature, Simulated Humidity, Simulated Soil Moisture**
  (`POST /plants/<id>/sensor/simulate`): `utils/sensor_simulator.py`
  generates one plausible reading per click, drifting slightly from the
  sensor's previous value so repeated readings look like a real pot
  gradually drying out rather than pure random noise. Trying to simulate a
  reading before pairing a sensor is rejected with a clear message.
- **Reading history**: the sensor page shows the 20 most recent readings
  in a table, with a "Dry" badge highlighting any moisture reading below
  the alert threshold used in Module 4's recommendation logic.
- **Documented amendment carried through from earlier in this build**: a
  "Simulated Light" reading was explicitly dropped in favor of moisture,
  temperature, and humidity only -- matching the `SensorReading` model
  that's been in the schema since Module 1's foundational setup, and the
  Context DFD's data flow.
- **The Module 4 payoff, verified directly**: before pairing a sensor, the
  Weather & Care page correctly showed "Not enough data yet." After
  pairing a sensor and simulating readings here in Module 5 -- with zero
  changes to any Module 4 file -- that same page automatically started
  returning a real recommendation (Water Today / Skip Watering / no
  action needed). This was confirmed by curl against the live app, not
  just by inspection.
- **Ownership-based access control carried over**: verified a second
  Gardener account gets a 404 trying to view, pair, or simulate readings
  on another Gardener's plant's sensor.

All of the above was exercised end-to-end with curl, including a full
regression pass confirming Modules 1-4 still work correctly afterward.

## What's implemented and verified in Module 4

- **Current Weather** (`GET /plants/<id>/weather`): live temperature,
  "feels like," humidity, description, and wind speed from OpenWeatherMap.
  Shows a clear warning banner instead of stale/fake data if no API key is
  set or the API call fails.
- **5-Day Forecast**: summarized from OpenWeatherMap's 3-hourly forecast
  into one row per day (min/max temp + rain expected), cached in the
  `WeatherForecast` table (D5 Weather Cache in the DFD) on every
  successful live call. Falls back to the last cache, or a clearly-labeled
  placeholder forecast if nothing has ever been cached for that location.
- **Plant Care Recommendation**: `utils/recommendation_engine.py` is a
  direct implementation of the Phase 03 Activity Diagram's branch
  structure (dry soil + no rain -> Water Today; rain expected -> Skip
  Watering; otherwise -> no action). **Important**: since the IoT Sensor
  Module (Module 5) hasn't been built yet, there's no way to pair a sensor
  to a plant yet, so `plant.sensor` is always `None` right now -- the
  recommendation engine correctly and consistently returns "Not enough
  data yet" until Module 5 exists. This is expected, documented behavior,
  not a bug, and the page says so directly. Nothing in Module 4 will need
  to change when Module 5 lands; real recommendations will just start
  appearing automatically.
- **Editable location**: since `Plant.location` is free text (e.g.
  "Balcony pot 1, south-facing") rather than a geocodable place, the
  weather page defaults to `DEFAULT_WEATHER_LOCATION` (`Dhaka,BD` unless
  you override it via the `DEFAULT_WEATHER_LOCATION` environment variable)
  and lets the Gardener type in a different `City,CountryCode` at any time.
- **Duplicate prevention**: reloading the weather page repeatedly does not
  spam the `CareRecommendation` table -- a new row is only inserted when
  the suggestion text actually changes from the last one saved for that
  plant. Verified directly against the database (4 page loads produced
  exactly 1 row, since the message was identical every time in the
  no-sensor-yet state).
- **Ownership-based access control carried over** from Modules 2 and 3:
  verified a second Gardener account gets a 404 trying to view another
  Gardener's plant's weather page.

All of the above was exercised end-to-end with curl, including a full
regression pass confirming Modules 1-3 still work correctly afterward
(login/logout, add/edit plant, and disease diagnosis all re-verified).

### Getting real weather data

**Recommended: use the `.env` file** (added after Module 6, so you don't
have to re-type `$env:OPENWEATHER_API_KEY` every time you open a new
terminal). Get a free key at https://openweathermap.org/api, then either:

- Edit the `.env` file already in the project root and put your key on
  the `OPENWEATHER_API_KEY=` line, or
- Copy `.env.example` to a new file named `.env` and fill it in yourself,
  if you removed the original.

`config.py` loads `.env` automatically on every startup (`python app.py`)
-- no environment variable needs to be set manually in the terminal
anymore. `.env` is listed in `.gitignore` so your real key never gets
committed or shared accidentally if you push this project to GitHub.

**Alternative (no `.env` file)**: you can still set it directly in the
terminal for one session, same as before:

```powershell
$env:OPENWEATHER_API_KEY = "your-key-here"
python app.py
```

Without a key configured either way, the app still works end-to-end
(placeholder forecast, no Current Weather card) -- exactly the same
"works now, upgrades automatically later" pattern used for Module 3's ML
model.

## What's implemented and verified in Module 7

- **Add Nursery Product Listing** (`GET/POST /nursery/products/add`,
  FR 1.1): category (Tool/Plant/Fertilizer), name, price, quantity, and
  an optional description. Nursery Owner-only -- a Gardener is redirected
  with a friendly message rather than shown a raw error, mirroring how
  Module 2 blocks Nursery Owners from Plant Management.
- **Edit Nursery Product Listing** (`GET/POST /nursery/products/<id>/edit`,
  FR 1.16, the amendment agreed on earlier in this build): same
  validation as Add, pre-filled form.
- **Delete Nursery Product Listing** (`POST /nursery/products/<id>/delete`,
  FR 1.17, the other amendment): Bootstrap modal confirmation, POST-only
  route, same pattern as Module 2's Delete Plant.
- **Browse Nursery Products** (`GET /marketplace`, FR 1.9): a
  Gardener-only catalog across *every* Nursery Owner's listings, with
  search-by-name and filter-by-category, showing which nursery each
  product belongs to.
- **Ownership-based access control, now proven across two different
  Nursery Owner accounts**: verified a second Nursery Owner gets a 404
  trying to edit or delete a product they don't own, and that the product
  survives the attempt untouched.
- **Role-gating verified in both directions** for the first time in this
  project: a Nursery Owner is blocked from Browse Products (a Gardener
  use case), and a Gardener is blocked from Add Product (a Nursery Owner
  use case) -- each with its own clear message.
- **`dashboard_redirect()` fully wired up**: Nursery Owners logging in now
  land directly on their Product Dashboard instead of the placeholder
  page from Module 1 -- the placeholder template file is still in the
  project (harmless, unused) but no route points to it anymore.

All of the above was exercised end-to-end with curl across three accounts
(two Nursery Owners + one Gardener), including a full regression pass
confirming Modules 1-6 still work correctly afterward.

## What's implemented and verified in Module 8

- **Display plant care information** (`GET /knowledge-base`,
  `GET /knowledge-base/<id>`): 24 articles auto-seeded on first startup
  (see `utils/seed_knowledge_base.py`), covering all 6 vegetables' disease
  labels from Module 3 plus 3 general-guidance articles (watering,
  reading diagnosis confidence scores, setting up alerts). Confirmed the
  seed runs exactly once -- calling it again on a later startup is a
  no-op, verified directly against the database.
- **Search and category filtering**, same UI pattern as Module 7's
  marketplace browse page for consistency: search by keyword (matches
  title or symptoms), filter by category (auto-populated from whatever
  categories actually exist in the table), or both together -- all
  verified to return the correct subset.
- **Independent from `utils/treatment_tips.py`** (Module 3), by design:
  that's a fast internal lookup used automatically during diagnosis; this
  is the user-facing, browsable reference library, built as its own
  module so a Gardener can look things up any time, not only right after
  a diagnosis.
- **Small, additive tie-in to Module 3**: the Disease Detection result
  page now has a "Learn more in the Knowledge Base" link that pre-fills a
  Knowledge Base search with the diagnosed disease's name -- one link
  added to `disease/result.html`, no route logic changed, verified by
  actually following the link end-to-end from a live diagnosis result.
- **Gardener-only**, matching the role-scoped pattern used for every
  other Gardener use case (Plant Management, Disease Detection, Weather,
  Sensors, Alerts) -- verified a Nursery Owner is redirected with a clear
  message.
- **Non-existent article IDs correctly 404**, and unauthenticated access
  correctly redirects to login with the right `?next=` parameter.

All of the above was exercised end-to-end with curl, including a full
regression pass confirming Modules 1-7 still work correctly afterward.

---

## Project complete

All 8 modules from the original specification are built, integrated, and
individually verified end-to-end, plus regression-tested against every
previously completed module at each step along the way. See "All 8
modules complete -- what's left" above for the remaining steps (mainly:
training the real ML model) before a final demo or submission.
