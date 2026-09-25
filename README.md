# birdsoftheworld-dataset-fairification

Cleans the messy `Birdsoftheworld.csv` into a structured dataset.

## Preprocessing

`preprocessing.py` reads `Birdsoftheworld.csv` and writes `outputs/Birdsoftheworld-preprocessed.csv` with the columns:

`species, location, time, description of bird, sex, feather color`

Because the source file is not valid CSV, the script repairs each row before splitting it:

- Strips the trailing padding commas added to every row.
- Splits off species, location and time using the `dd-mm-yyyy hh:mm` timestamp as an anchor, so locations containing commas (`Washington, D.C.`) stay intact.
- Finds the last `Male`/`Female`/`Unknown` value in each row and uses it as the anchor to separate description from sex and feather color.
- Cuts duplicated `...,<sex>,<color>` tails that corruption left inside some descriptions.
- Repairs broken quoting: `""` escapes are turned back into `"`, leftover structural quotes are removed.
- Fallback: rows without a recognisable sex get empty sex/color fields.

Run with:

```bash
python3 preprocessing.py
```

## Description feature extraction

`extract_description_features.py` reads `outputs/Birdsoftheworld-preprocessed.csv` and
writes `outputs/Birdsoftheworld-features.csv`, retaining the input columns and appending
one categorical column per _observed_ trait type (such as `size`,
`plumage_color`, `head_color`, `bill_shape`, and `vocalization`). Cells contain
normalized values such as `small`, `white`, or `hooked`, not true/false flags.
Where a description explicitly mentions more than one value for the same trait,
the cell contains sorted values separated by `|`, e.g. `plumage_color=black|white`.
Split on `|` before ontology mapping. A blank is unknown, not a negative
assertion. The original description stays available for review.

```bash
python3 extract_description_features.py --report
python3 -m unittest test_extract_description_features.py
```

The report is saved to `outputs/description-feature-analysis.md` and contains row
frequencies and the number of distinct species mentioning each column/value
pair. Neither the feature names nor frequencies imply validated ontology mappings
or biological prevalence. Defaults write into `outputs/`; explicit `--output`
and `--report <path>` arguments can override those destinations. The observed
feature columns may change for different inputs.
