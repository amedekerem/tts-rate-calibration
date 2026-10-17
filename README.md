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

## Three-Slide Run Log

## Review Notes

## App Results
