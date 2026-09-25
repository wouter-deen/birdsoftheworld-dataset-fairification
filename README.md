# birdsoftheworld-dataset-fairification

Cleans the messy `Birdsoftheworld.csv` into a structured dataset.

## Preprocessing

`preprocessing.py` reads `Birdsoftheworld.csv` and writes `Birdsoftheworld-preprocessed.csv` with the columns:

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
