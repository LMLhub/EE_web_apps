# The Boundary Experiment

A small, dependency-free local app based on the supplied additive gambles and the Qualtrics survey **Experiment Boundaries 2023 – APP** (`SV_86Wv8Qdsl4r5aKi`), inspected in Chrome on 23 October 2026. The entry modes and local results experience are inspired by [ErgEx](https://apps.ergodicityeconomics.com/ergex/).

## Open the app

Double-click **Start Experiment.command**, or open **index.html** in Chrome. Everything works directly from the folder, offline. There is nothing to install.

For a local HTTP server, with Node installed:

```sh
npm start
```

Open **http://127.0.0.1:4173**. The server binds only to this computer. Set `PORT` to use a different port. Stop it with Ctrl+C.

Browser storage is specific to the browser and origin. Opening the file directly and using the HTTP server have separate saved runs. Keep using the same launch method to resume a run. Only the latest run is retained; the app offers an export before replacing it. Version 1.2 keeps existing 1.0 and 1.1 saved runs readable. An untouched 1.0 run adopts scripted learning; a run with recorded decisions retains its original random practice to avoid mixing protocols. Start a new run to apply the new learning protocol to the whole run.

## What is preserved

- All 30 supplied gamble pairs, including outcome order. Both outcomes have probability 0.5.
- Three independent sessions, each starting at zero, with up to 30 decisions in full mode.
- No boundary first; upper/lower session order randomly assigned for each run. The survey's between-participant even-presentation allocation is replaced by an independent fair random assignment because there is no shared participant database.
- The no-boundary and upper-boundary sessions use gamble pairs 1–30 in the supplied order. The lower-boundary session shuffles all 30. This matches the exported active block randomization settings, which differ between conditions.
- Randomized left/right option placement on every trial. Within each option, the supplied outcome order is preserved.
- Three seconds per decision; the final selected gamble counts. Selections can be revised until the deadline. A missed choice receives the minimum across all four displayed outcomes.
- No running wealth or outcome feedback in timed sessions. Wealth resets between sessions.
- Strict upper/lower crossings: **above +2,000** or **below −2,000** ends the relevant session and records exactly that boundary. Reaching exactly the boundary is not a crossing. The source instructions say “above/below,” while comprehension questions more loosely say “hit”; this implementation follows the explicit instruction text.
- General and boundary comprehension checks, with one retry and termination after two incorrect responses. Boundary checks are omitted in the explicitly shortened presentation demo.

## Local adaptations

- A guided tour and presentation demo each use eight gamble pairs per session. For no-boundary and upper sessions these are pairs 1, 5, 9, 13, 17, 21, 25, 30; for lower, eight from a shuffled order. Full mode uses every pair.
- Full mode has eight untimed learning decisions; guided mode uses the first three. Learning follows the active Qualtrics loop’s fixed sign sequence: **win, loss, win, loss, loss, win, win, win** (QID837–841, QID857–859). The selected gamble determines the amount. The app keeps its existing practice pairs rather than substituting Qualtrics’ separate practice image amounts. Learning has visible wealth and a trajectory chart and is excluded from timed results. A “Skip practice rounds” button during practice or its feedback advances to the first session. Completed practice decisions remain saved; JSON records the skipped count and time. The first timed session still starts at zero.
- The survey records timed choices without JavaScript applying outcomes or stopping the active timed blocks. The local app implements the absorbing boundaries described in the participant instructions: it draws the outcomes and ends the session on a crossing.
- Prolific ID, recruitment consent, CAPTCHA, redirects, and real payments are omitted. This app is a local simulation with a clearly labelled hypothetical bonus.
- Results include a short choice diagnostic per setting: risky-choice percentage, numerator and denominator, lower-risk and missed counts, and a percentage-point comparison with the no-boundary setting. “Risky” means the larger absolute outcome in the offered pair, before applying the boundary. Only answered timed trials enter the percentage; practice, missed choices, and unplayed trials after absorption are excluded. No answered trials produces an unavailable percentage, not 0%. Interrupted trials with a recorded selection are included and their count is disclosed. These are descriptive outputs, not fitted risk-preference estimates. Wealth trajectories and final points are also shown. The chart displays one selected session at a time, with only its applicable boundary: none for the unbounded session or practice, +2,000 for upper, and −2,000 for lower. During play, the session progress strip names only the current condition.
- When a timed tab is hidden, exited, or reloaded, the current trial is resolved with its last selection (or the missed-choice penalty), flagged `interrupted`, and the app pauses before the next trial. No hidden trials run in the background. Such interrupted runs should not be treated as uninterrupted laboratory observations.

## Visual design

The interface follows the LML / ErgEx visual reference: a navy welcome panel, gold sans-serif headings, translucent rectangular mode cards, and dark blue pill controls. Active games use a black stage, two columns of numerical outcomes, and a gold selection outline. Instructions use a white rounded panel on black. Numeric gamble outcomes remain explicit; the Copenhagen experiment's learned fractal cues are not introduced into this protocol.

## Randomness

For every answered timed decision, `app.js` requests a fresh unsigned 32-bit value from `crypto.getRandomValues`. Values below half the range select the first outcome; values in the other half select the second. Each therefore has probability 0.5. Timed sessions have no scripted sequence, forced balancing of wins and losses, or dependence on previous outcomes. Learning rounds use the separate fixed sequence described above and consume no random outcome draws. This is cryptographically secure pseudorandomness supplied by the browser, not a physical random-number device.

The payoff amounts are the fixed supplied pairs. The random session order, left/right placements, and lower-boundary trial shuffle come from a seeded generator initialized with a fresh cryptographic seed. The unbounded and upper-boundary trial orders are intentionally fixed to match Qualtrics. Missing responses are intentionally deterministic: they receive the worst available outcome.

## Hypothetical bonus

Before play, participants are told that more final points produce a larger hypothetical bonus, up to £3 per setting and £9 in total. No money is paid. After all three sessions, results show the total and each setting’s amount before the choice diagnostic. Incomplete runs do not display a total bonus or assign £0 to unfinished settings.

The paper *The London Experiment*, supplied 27 October 2026, gives the formula `£3 × (final points − min) / (max − min)` on page 7, but does not define the reference extrema. This app uses that formula with **app-defined theoretical ranges**, not a claim to reconstruct the original participants’ exact payments. The user authorized choosing these ranges. The study’s £2.25 participation payment is not included.

For the full experiment, the sum of the largest absolute outcome from each of the 30 pairs is 21,053 points:

| Setting | Minimum (£0) | Maximum (£3) |
| --- | ---: | ---: |
| No boundary | −21,053 | +21,053 |
| Upper boundary | −21,053 | +2,000 |
| Lower boundary | −2,000 | +21,053 |

The range uses all **scheduled** gambles, including any that go unplayed after absorption. It never depends on choices, realized outcomes, practice, a leaderboard, or a personal best. For short modes it is calculated from the eight scheduled gambles, so those amounts are labelled as an illustration on the shorter mode’s scale. Upper absorption maps to £3; lower absorption maps to £0. This normalization also means that zero points maps to different bonus amounts across settings; no common points-to-pounds rate is implied.

Scores above the configured maximum receive £3 and scores below the minimum receive £0. The score is clamped before conversion without changing the recorded points, so even extreme finite values cannot overflow the calculation. Invalid scores or zero-width ranges return an unavailable bonus. Each setting is rounded to the nearest penny and the total adds those rounded amounts, always between £0 and £9. `BONUS_RULE` identifies the calculation as `theoretical-range-v1`. New runs record `bonusFraming` when created. Older runs keep their original version and observations; their results can be evaluated retrospectively, with a visible note that the framing was added after the run was created. No leaderboard or personal-best incentive is introduced.

## Data

No network requests, analytics, external fonts, or third-party scripts are used by the app. The app has no external links. The run is stored in `localStorage` under `boundary-experiment-v1`.

**CSV** contains one row per played timed decision: run/mode/seed, condition and session index, trial and gamble ID, displayed options and outcomes, final selection, missed flag, first and last selection times, selection count/history, sampled outcome, raw and bounded wealth, absorption, interruption, and timestamps.

**JSON** additionally includes `hypotheticalBonus` (currency, rule, fixed ranges, final points, per-setting amounts and total in integer pennies, and whether bonus framing was present when the run was created), plus `choiceDiagnostic` (per-setting counts, exact unrounded percentages, baseline differences, and denominator definition), the whole randomized schedule, practice, comprehension checks, completion status, protocol metadata, and the original gamble list. Practice records include `outcomeMode` and `scriptStep`, and the protocol includes the fixed practice signs. The schedule seed reproduces assignment, not the coin draws: outcomes use the browser's cryptographic random generator and are retained in the export.

Unplayed trials after absorption remain in the scheduled trial list but have no result rows. They remain part of the fixed bonus range. No payments are made.

## Files and checks

- `index.html`, `styles.css`: layout and styling.
- `engine.js`: gamble data, reproducible schedule, payoff and boundary rules, CSV export.
- `app.js`: interaction, timers, saving, charts, and downloads.
- `server.js`: optional Node static server; no package dependencies.
- `tests/engine.test.js`: boundary edge cases, missing responses, schedule fidelity, and 100 simulated runs.

Run `npm test` to execute the engine checks.
