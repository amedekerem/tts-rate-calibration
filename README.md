# TTS Rate Calibration

## Calibration

- **Voice Used:** `en-US-AriaNeural` (`edge-tts`)
- **Word Counting Rule:** Split passage text on spaces (`passage_text.split(" ")`)
- **Failures and Exclusions:** If any row fails during synthesis or audio length inspection, its error is printed and the row is excluded from the overall average words per second calculation. In this calibration run, all 8 passages (`p01`–`p08`) succeeded with 0 failures and 0 exclusions.

### Calibration Output

```text
p01, 25, 8.98, 2.79
p02, 59, 21.48, 2.75
p03, 22, 9.60, 2.29
p04, 80, 29.76, 2.69
p05, 31, 13.49, 2.30
p06, 71, 27.77, 2.56
p07, 47, 17.95, 2.62
p08, 89, 31.03, 2.87
Average words per second: 2.61
```

| Passage ID | Word Count | Duration (s) | Words / Sec |
| :--- | :---: | :---: | :---: |
| `p01` | 25 | 8.98 | 2.79 |
| `p02` | 59 | 21.48 | 2.75 |
| `p03` | 22 | 9.60 | 2.29 |
| `p04` | 80 | 29.76 | 2.69 |
| `p05` | 31 | 13.49 | 2.30 |
| `p06` | 71 | 27.77 | 2.56 |
| `p07` | 47 | 17.95 | 2.62 |
| `p08` | 89 | 31.03 | 2.87 |
| **Average** | — | — | **2.61** |

### Calibration Passages (Full Text)

- **`p01`**: Revenue climbed steadily through the quarter, then jumped sharply in March as the new plan launched, lifting monthly totals to their highest point this year.
- **`p02`**: This funnel shows how visitors move from the pricing page to a paid plan. About ten thousand people viewed pricing in February. Just under four thousand started a free trial, and roughly nine hundred went on to pay. The biggest drop happens between the trial and the first payment, so that step is where the team will focus next.
- **`p03`**: This pie chart splits new sign-ups by source. Organic search brings in almost half, with referrals and paid ads sharing the rest.
- **`p04`**: This chart combines two measures from the support team. The bars show how many tickets arrived each week, and the line shows the average time to a first reply. Ticket volume stayed between roughly eleven and thirteen hundred a week for the whole period. Even so, reply times fell from about nine hours in early February to under four hours by mid March. The team handled the same workload much faster, mostly because common questions now get an instant answer.
- **`p05`**: This slide walks through three regions. Growth was strongest in Asia Pacific, where sign-ups nearly doubled between January and March, while Europe held flat and North America dipped slightly before recovering.
- **`p06`**: Here the stacked bars break down average monthly spend per team account. In January the typical account paid $48, mostly on seats. By March that rose to $61, and nearly all of the extra came from the new add-ons shown in green. Seat spending barely moved. So the growth is not coming from bigger teams, it is coming from teams buying more features on top of the plan they already have.
- **`p07`**: Costs stayed under control all year. The bar chart shows spending on each team holding within budget, with only marketing rising slightly in the final quarter. That increase paid for the spring campaign, and it still left the company around four percent under its total annual plan.
- **`p08`**: The map on this slide shades each country by how many templates were used in the last six weeks. Darker colours mean more use. The United States and India stand out as the two darkest areas, but the fastest change is in Brazil and Indonesia, where usage grew by more than half since the start of February. Australia is smaller in total, yet it has the highest use per person of any market. If we want feedback on new templates, these four countries are the clearest places to start.

## Pipeline Spec

This spec defines how the Slide narration app turns one slide image and a target length in seconds into a narrated MP3 file that runs within 3 seconds of that target.

### 1. Model prompt (verbatim)

The app sends this text to the vision model through OpenRouter, along with the slide image. A vision model is an AI model that reads images as well as text. The app reads the model id from the `OPENROUTER_MODEL` setting in the local environment file and never hardcodes it. At run time the app fills in one value, `{target_words}`. Each sample slide in `canva_create_sample_slides.csv` has a `key_visual_point` column. The app never puts that value in the prompt and uses it only to score the finished script in section 4.

```
You are writing a spoken voiceover for the presentation slide in the attached image.
Start with what the chart, graph or main picture shows. Say the main change, trend or comparison in plain words, using the numbers you can read on it.
Only after that, cover the slide's title and written text.
Write about {target_words} words in total.
Write in short, natural spoken sentences, as one paragraph.
Do not say "this slide", "as you can see" or "in this image".
Do not read out axis labels, legends or every number one by one.
Return only the script text, with nothing before or after it.
```

### 2. Length formula

| Item | Value |
|---|---|
| Formula | target words = target seconds × 2.61 words per second |
| Rate | 2.61 words per second. This is the average from the edge-tts calibration run: 8 test scripts, voice `en-US-AriaNeural`, rate `+0%` |
| Rounding | Round to the nearest whole word. Exact halves round up. |
| Worked example | 30 seconds × 2.61 words per second = 78.3 → **78 words** |
| Gap | gap = MP3 length measured by mutagen (seconds) - target seconds |

A positive gap means the audio runs too long. A negative gap means it runs too short.

### 3. Retry order and limit

The app runs a retry each time the gap is more than 3.0 seconds either way. Each retry is one action.

| Order | Step | Detail |
|---|---|---|
| 1 | edge-tts rate nudge | The script stays the same. The app changes the edge-tts speaking rate by 10 points and makes the MP3 again. If the gap is over +3.0 s, the rate goes faster (`+10%`). If the gap is under -3.0 s, the rate goes slower (`-10%`). The rate never moves more than 20 points from `+0%`, so this step can run at most 2 times. |
| 2 | Model rewrite | This step runs only if the audio still misses after the rate nudges. The rate resets to `+0%`. The app sends the script back with the rewrite prompt below. It sets new target words to the current word count - round(gap × 2.61). |

Rewrite prompt (verbatim):

```
Rewrite this voiceover script in about {target_words} words.
Keep the chart or main picture first. Keep the same facts and numbers.
Return only the script text.

Script: {script}
```

| Rule | Value |
|---|---|
| Retry limit | 4 retries after the first attempt: up to 2 rate nudges, then up to 2 model rewrites |
| Limit reached with no timing pass | The app marks the run **failed**. It keeps the last script and MP3 in the log. It shows no download button. It shows this message: "Couldn't fit this narration within 3 seconds of {target} seconds. Last attempt: {measured} seconds." |

### 4. Pass / fail rule

| Rule | Value |
|---|---|
| Timing pass | The gap is between -3.0 and +3.0 seconds, including exactly -3.0 and +3.0 |
| How length is measured | The app reads the length with `mutagen.mp3.MP3(path).info.length` on the saved MP3 file. It rounds the result to 0.1 seconds. |
| Not allowed | Estimating the length from the word count or from the target words |
| Coverage pass | The script states the slide's `key_visual_point`: the same fact, with the same direction and the same numbers. For example, "sales doubled after March" passes. "Sales changed over the year" fails. |
| Coverage check | The script is compared against `key_visual_point` after the run. The model never sees that value. |
| Failing runs | The app logs every failed run and shows it in the results table. It never drops, hides or quietly re-runs a failed run past the retry limit. |

The results table has these columns: `slide_id`, `target_length_seconds`, `measured_seconds`, `gap_seconds`, `retries_used`, `timing_verdict`, `coverage_verdict`.

### 5. Download rule

| Rule | Value |
|---|---|
| When the download appears | Only after the latest MP3 passes timing under section 4 |
| Before the timing pass | The audio player can play the current attempt. The app hides the download button. |
| After the timing pass | The app shows the download button for that exact MP3, with the measured length and the target side by side |
| Retry limit reached with no pass | The run is marked failed. The download button never appears. The failure message from section 3 is shown. |
| Coverage failure with a timing pass | The download still appears. The results table marks the row `coverage_verdict = FAIL`. |

## Three-Slide Run Log

## Review Notes

## App Results
