# Sampling Rationale

This study begins with the PJIP-derived journal universe as a raw intake population, but the analyzed population for the journal-documentation audit is narrower: English-language or English-accessible peer-reviewed philosophy journals that publish ordinary research articles.

## Population and target precision

- Raw PJIP intake population: `N = 274`
- Current confirmed analyzed population for documentation sampling: `N = 150`
- Unresolved language-accessibility cases after the first-pass audit: `124`
- Confidence level: `95%`
- Assumed response distribution: `p = 0.5`
- Target margin of error: `+/-10%`

The first-pass language audit identifies a confirmed English-eligible subset of 150 journals. A conservative sample can therefore be drawn from that confirmed subset now, while unresolved multilingual or inaccessible cases remain outside the analyzed population until manually adjudicated.

## Formula

Finite-population correction:

`n = n0 / (1 + ((n0 - 1) / N))`

Unadjusted sample size:

`n0 = z^2 * p * (1 - p) / e^2`

Using `z = 1.96`, `p = 0.5`, and `e = 0.10`, the current confirmed eligible population `N = 150` yields:

- `n0 = 96.04`
- `n = 96.04 / (1 + ((96.04 - 1) / 150)) = 58.79`
- Rounded-up sample size: `59`

## Reference values

- If `N = 200`: `+/-10%` requires `66`, `+/-7.5%` requires `92`, `+/-5%` requires `132`
- If `N = 175`: `+/-10%` requires `62`, `+/-7.5%` requires `87`, `+/-5%` requires `121`
- If `N = 150`: `+/-10%` requires `59`, `+/-7.5%` requires `82`, `+/-5%` requires `108`
- If `N = 125`: `+/-10%` requires `55`, `+/-7.5%` requires `75`, `+/-5%` requires `94`
- If `N = 100`: `+/-10%` requires `49`, `+/-7.5%` requires `63`, `+/-5%` requires `80`

## Allocation rule

Once language eligibility is coded, the sampling script uses proportional stratified allocation over the eligible `primary_category` strata in the journal universe. With the present PJIP import, the current raw strata are:

- `generalist`: 76 journals
- `specialist`: 198 journals

After the first-pass language filter, the confirmed eligible strata are:

- `generalist`: 39 journals -> sample target `15`
- `specialist`: 111 journals -> sample target `44`

## Methodological note

Non-English journals are not treated as lower quality or irrelevant. They are excluded from the analyzed population when the study cannot code their policies or article materials reliably in the original language. All language-based exclusions should be catalogued in the journal-universe files.

At the current stage, journals with unresolved English accessibility are also held out rather than assumed eligible. This makes the present `N = 150` and `n = 59` figures conservative first-pass values.