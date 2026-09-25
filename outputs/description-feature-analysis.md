# Bird description feature analysis

Source: `outputs/Birdsoftheworld-preprocessed.csv` (1,310 rows, 534 species; 1,310 nonempty descriptions).

## Method

Counts below are **rows with an explicit textual mention**, not biological prevalence. A description can mention multiple colors/traits; columns are non-exclusive. Color is bound to its named body part (e.g. `head_color=white`), while `plumage_color=white` is reserved for explicitly general plumage/feather wording. Mixed gray-brown and blue-gray are kept as separate named shades; black-and-white is split into black and white. Ruby-red/crimson map to red; spelling variants and plurals are normalized. Each feature column holds its value (e.g. `size=small`); explicit multiple values are sorted and joined with `|` (e.g. `plumage_color=black|white`). A blank means unmentioned (unknown, **not false**), and `|` is not part of any individual value. The original description and other input columns are retained.

Rules are intentionally conservative and do not infer traits from the species, the separate `feather color` column, or a habitat inferred from a bird group. They do not resolve negation, uncertainty, or every possible paraphrase. Check the original description before linking traits to ontologies; a different source row is not an independent observation of a species.

Categorical columns: **49**; distinct observed column/value pairs: **244**. Rows with at least one feature: **1,310/1,310**. The species count measures how broadly a feature is mentioned across distinct species; low species counts can indicate distinctive wording but do not establish biological uniqueness.

## Most frequently mentioned atomic values

| Column | Value | Rows | % rows | Species |
| --- | --- | ---: | ---: | ---: |
| `size` | `medium` | 615 | 46.9% | 255 |
| `size` | `small` | 466 | 35.6% | 207 |
| `plumage_color` | `brown` | 269 | 20.5% | 156 |
| `vocalization` | `call` | 254 | 19.4% | 123 |
| `plumage_color` | `white` | 251 | 19.2% | 124 |
| `plumage_color` | `black` | 229 | 17.5% | 102 |
| `size` | `large` | 196 | 15.0% | 100 |
| `plumage_color` | `green` | 109 | 8.3% | 46 |
| `plumage_color` | `gray` | 103 | 7.9% | 60 |
| `plumage_color` | `gray_brown` | 102 | 7.8% | 57 |
| `underparts_color` | `white` | 102 | 7.8% | 68 |
| `head_ornament` | `crest` | 99 | 7.6% | 36 |
| `plumage_color` | `blue` | 88 | 6.7% | 40 |
| `plumage_pattern` | `mottled` | 83 | 6.3% | 52 |
| `vocalization` | `song` | 83 | 6.3% | 52 |
| `plumage_color` | `yellow` | 78 | 6.0% | 28 |
| `locomotion` | `wading` | 71 | 5.4% | 33 |
| `plumage_color` | `red` | 57 | 4.4% | 30 |
| `cap_color` | `black` | 53 | 4.0% | 25 |
| `bill_color` | `yellow` | 41 | 3.1% | 24 |
| `head_color` | `black` | 39 | 3.0% | 24 |
| `throat_color` | `red` | 39 | 3.0% | 9 |
| `bill_length` | `long` | 36 | 2.7% | 21 |
| `locomotion` | `diving` | 36 | 2.7% | 20 |
| `head_color` | `white` | 32 | 2.4% | 17 |
| `bill_shape` | `slender` | 31 | 2.4% | 16 |
| `bill_color` | `red` | 31 | 2.4% | 19 |
| `plumage_finish` | `iridescent` | 29 | 2.2% | 14 |
| `back_color` | `gray` | 26 | 2.0% | 15 |
| `body_color` | `brown` | 22 | 1.7% | 16 |

## Repeated but relatively concentrated mentions

Traits mentioned in at least 10 rows but across at most 10 species, ranked by row count. Repeated descriptions can inflate row counts; these are leads for review, not measures of species specificity.

| Column | Value | Rows | % rows | Species |
| --- | --- | ---: | ---: | ---: |
| `throat_color` | `red` | 39 | 3.0% | 9 |
| `plumage_color` | `blue_gray` | 21 | 1.6% | 9 |
| `bill_length` | `short` | 20 | 1.5% | 1 |
| `head_color` | `red` | 17 | 1.3% | 9 |
| `plumage_color` | `orange` | 17 | 1.3% | 10 |
| `throat_color` | `white` | 16 | 1.2% | 9 |
| `wing_color` | `white` | 16 | 1.2% | 10 |
| `head_ornament` | `ear_tufts` | 16 | 1.2% | 6 |
| `plumage_color` | `pink` | 15 | 1.1% | 7 |
| `plumage_pattern` | `barred` | 15 | 1.1% | 8 |
| `back_color` | `green` | 14 | 1.1% | 10 |
| `bill_color` | `black` | 14 | 1.1% | 6 |
| `crown_color` | `red` | 14 | 1.1% | 5 |
| `plumage_color` | `purple` | 14 | 1.1% | 5 |
| `behavior` | `courtship_display` | 13 | 1.0% | 10 |

## Less common, potentially distinguishing traits

Examples with at least two mentions, ranked by fewest species then most rows; rarity in this dataset is not proof of diagnostic value.

| Column | Value | Rows | % rows | Species |
| --- | --- | ---: | ---: | ---: |
| `bill_length` | `short` | 20 | 1.5% | 1 |
| `cheek_color` | `white` | 6 | 0.5% | 1 |
| `bill_color` | `white` | 4 | 0.3% | 1 |
| `body_color` | `pink` | 4 | 0.3% | 1 |
| `side_color` | `chestnut` | 4 | 0.3% | 1 |
| `side_color` | `red` | 4 | 0.3% | 1 |
| `nape_color` | `gold` | 3 | 0.2% | 1 |
| `nape_color` | `gray` | 3 | 0.2% | 1 |
| `tail_color` | `rust` | 3 | 0.2% | 1 |
| `throat_color` | `pink` | 3 | 0.2% | 1 |
| `cheek_color` | `black` | 2 | 0.2% | 1 |
| `cheek_color` | `blue` | 2 | 0.2% | 1 |
| `cheek_color` | `chestnut` | 2 | 0.2% | 1 |
| `chin_color` | `black` | 2 | 0.2% | 1 |
| `crown_color` | `rust` | 2 | 0.2% | 1 |
| `foot_color` | `yellow` | 2 | 0.2% | 1 |
| `nape_color` | `brown` | 2 | 0.2% | 1 |
| `rump_color` | `yellow` | 2 | 0.2% | 1 |
| `side_color` | `white` | 2 | 0.2% | 1 |
| `tail_color` | `blue` | 2 | 0.2% | 1 |

## Complete column/value inventory

These are all observed values within the categorical columns. Counts include duplicate descriptions/rows; `Species` deduplicates species names.

| Column | Value | Rows | % rows | Species |
| --- | --- | ---: | ---: | ---: |
| `size` | `medium` | 615 | 46.9% | 255 |
| `size` | `small` | 466 | 35.6% | 207 |
| `plumage_color` | `brown` | 269 | 20.5% | 156 |
| `vocalization` | `call` | 254 | 19.4% | 123 |
| `plumage_color` | `white` | 251 | 19.2% | 124 |
| `plumage_color` | `black` | 229 | 17.5% | 102 |
| `size` | `large` | 196 | 15.0% | 100 |
| `plumage_color` | `green` | 109 | 8.3% | 46 |
| `plumage_color` | `gray` | 103 | 7.9% | 60 |
| `plumage_color` | `gray_brown` | 102 | 7.8% | 57 |
| `underparts_color` | `white` | 102 | 7.8% | 68 |
| `head_ornament` | `crest` | 99 | 7.6% | 36 |
| `plumage_color` | `blue` | 88 | 6.7% | 40 |
| `plumage_pattern` | `mottled` | 83 | 6.3% | 52 |
| `vocalization` | `song` | 83 | 6.3% | 52 |
| `plumage_color` | `yellow` | 78 | 6.0% | 28 |
| `locomotion` | `wading` | 71 | 5.4% | 33 |
| `plumage_color` | `red` | 57 | 4.4% | 30 |
| `cap_color` | `black` | 53 | 4.0% | 25 |
| `bill_color` | `yellow` | 41 | 3.1% | 24 |
| `head_color` | `black` | 39 | 3.0% | 24 |
| `throat_color` | `red` | 39 | 3.0% | 9 |
| `bill_length` | `long` | 36 | 2.7% | 21 |
| `locomotion` | `diving` | 36 | 2.7% | 20 |
| `head_color` | `white` | 32 | 2.4% | 17 |
| `bill_shape` | `slender` | 31 | 2.4% | 16 |
| `bill_color` | `red` | 31 | 2.4% | 19 |
| `plumage_finish` | `iridescent` | 29 | 2.2% | 14 |
| `back_color` | `gray` | 26 | 2.0% | 15 |
| `body_color` | `brown` | 22 | 1.7% | 16 |
| `underparts_color` | `rust` | 22 | 1.7% | 14 |
| `underparts_color` | `yellow` | 22 | 1.7% | 17 |
| `neck_length` | `long` | 22 | 1.7% | 12 |
| `plumage_color` | `blue_gray` | 21 | 1.6% | 9 |
| `bill_length` | `short` | 20 | 1.5% | 1 |
| `bill_shape` | `curved` | 20 | 1.5% | 15 |
| `back_color` | `black` | 20 | 1.5% | 15 |
| `height` | `tall` | 20 | 1.5% | 11 |
| `tail_length` | `long` | 20 | 1.5% | 12 |
| `leg_length` | `long` | 19 | 1.5% | 11 |
| `head_marking` | `mask` | 18 | 1.4% | 13 |
| `tail_shape` | `forked` | 18 | 1.4% | 12 |
| `body_color` | `gray` | 17 | 1.3% | 14 |
| `body_color` | `white` | 17 | 1.3% | 16 |
| `head_color` | `red` | 17 | 1.3% | 9 |
| `plumage_color` | `orange` | 17 | 1.3% | 10 |
| `throat_color` | `white` | 16 | 1.2% | 9 |
| `wing_color` | `white` | 16 | 1.2% | 10 |
| `head_ornament` | `ear_tufts` | 16 | 1.2% | 6 |
| `back_color` | `brown` | 15 | 1.1% | 12 |
| `plumage_color` | `pink` | 15 | 1.1% | 7 |
| `plumage_pattern` | `barred` | 15 | 1.1% | 8 |
| `plumage_pattern` | `streaked` | 15 | 1.1% | 13 |
| `back_color` | `green` | 14 | 1.1% | 10 |
| `bill_color` | `black` | 14 | 1.1% | 6 |
| `crown_color` | `red` | 14 | 1.1% | 5 |
| `plumage_color` | `purple` | 14 | 1.1% | 5 |
| `behavior` | `courtship_display` | 13 | 1.0% | 10 |
| `face_color` | `white` | 13 | 1.0% | 10 |
| `habitat_preference` | `coastal` | 13 | 1.0% | 13 |
| `bill_shape` | `hooked` | 12 | 0.9% | 11 |
| `bill_shape` | `spoon` | 12 | 0.9% | 3 |
| `body_color` | `black` | 12 | 0.9% | 10 |
| `eye_color` | `red` | 12 | 0.9% | 7 |
| `eye_color` | `yellow` | 12 | 0.9% | 9 |
| `wing_color` | `black` | 12 | 0.9% | 8 |
| `head_color` | `gray` | 11 | 0.8% | 6 |
| `head_color` | `yellow` | 11 | 0.8% | 7 |
| `plumage_pattern` | `spotted` | 11 | 0.8% | 6 |
| `back_color` | `blue_gray` | 10 | 0.8% | 6 |
| `crest_color` | `red` | 10 | 0.8% | 4 |
| `face_color` | `black` | 10 | 0.8% | 10 |
| `rump_color` | `white` | 10 | 0.8% | 6 |
| `tail_color` | `red` | 10 | 0.8% | 4 |
| `throat_color` | `black` | 10 | 0.8% | 6 |
| `underparts_color` | `red` | 10 | 0.8% | 5 |
| `plumage_pattern` | `striped` | 10 | 0.8% | 6 |
| `bill_shape` | `upturned` | 9 | 0.7% | 5 |
| `back_color` | `white` | 9 | 0.7% | 6 |
| `bill_color` | `orange` | 9 | 0.7% | 6 |
| `underparts_color` | `orange` | 9 | 0.7% | 5 |
| `bill_shape` | `dagger` | 8 | 0.6% | 3 |
| `crown_color` | `yellow` | 8 | 0.6% | 5 |
| `shoulder_color` | `red` | 8 | 0.6% | 3 |
| `flight_style` | `soaring` | 8 | 0.6% | 5 |
| `bill_shape` | `downcurved` | 7 | 0.5% | 4 |
| `breast_color` | `red` | 7 | 0.5% | 4 |
| `cap_color` | `red` | 7 | 0.5% | 3 |
| `crown_color` | `black` | 7 | 0.5% | 6 |
| `crown_color` | `gold` | 7 | 0.5% | 2 |
| `crown_color` | `white` | 7 | 0.5% | 5 |
| `leg_color` | `pink` | 7 | 0.5% | 2 |
| `upperparts_color` | `black` | 7 | 0.5% | 4 |
| `upperparts_color` | `blue` | 7 | 0.5% | 5 |
| `head_marking` | `eye_ring` | 7 | 0.5% | 6 |
| `breast_color` | `orange` | 6 | 0.5% | 6 |
| `cheek_color` | `white` | 6 | 0.5% | 1 |
| `crest_color` | `black` | 6 | 0.5% | 5 |
| `eye_color` | `white` | 6 | 0.5% | 4 |
| `neck_color` | `chestnut` | 6 | 0.5% | 2 |
| `neck_color` | `white` | 6 | 0.5% | 3 |
| `plumage_color` | `chestnut` | 6 | 0.5% | 3 |
| `plumage_color` | `rufous` | 6 | 0.5% | 2 |
| `plumage_color` | `rust` | 6 | 0.5% | 5 |
| `tail_color` | `white` | 6 | 0.5% | 5 |
| `throat_color` | `yellow` | 6 | 0.5% | 4 |
| `flight_style` | `hovering` | 6 | 0.5% | 4 |
| `leg_covering` | `feathered` | 6 | 0.5% | 4 |
| `activity_period` | `nocturnal` | 5 | 0.4% | 4 |
| `body_color` | `red` | 5 | 0.4% | 5 |
| `face_color` | `yellow` | 5 | 0.4% | 4 |
| `foot_color` | `red` | 5 | 0.4% | 2 |
| `leg_color` | `black` | 5 | 0.4% | 3 |
| `leg_color` | `yellow` | 5 | 0.4% | 3 |
| `underparts_color` | `black` | 5 | 0.4% | 2 |
| `upperparts_color` | `blue_gray` | 5 | 0.4% | 3 |
| `wing_color` | `gray` | 5 | 0.4% | 5 |
| `habitat_preference` | `freshwater` | 5 | 0.4% | 5 |
| `habitat_preference` | `wetland` | 5 | 0.4% | 5 |
| `behavior` | `scavenging` | 4 | 0.3% | 2 |
| `back_color` | `blue` | 4 | 0.3% | 3 |
| `back_color` | `gray_brown` | 4 | 0.3% | 4 |
| `bill_color` | `white` | 4 | 0.3% | 1 |
| `body_color` | `pink` | 4 | 0.3% | 1 |
| `body_color` | `yellow` | 4 | 0.3% | 3 |
| `breast_color` | `rust` | 4 | 0.3% | 4 |
| `cap_color` | `rust` | 4 | 0.3% | 3 |
| `collar_color` | `black` | 4 | 0.3% | 3 |
| `head_color` | `blue` | 4 | 0.3% | 2 |
| `head_color` | `green` | 4 | 0.3% | 3 |
| `neck_color` | `red` | 4 | 0.3% | 3 |
| `plumage_color` | `copper` | 4 | 0.3% | 2 |
| `side_color` | `chestnut` | 4 | 0.3% | 1 |
| `side_color` | `red` | 4 | 0.3% | 1 |
| `tail_color` | `black` | 4 | 0.3% | 4 |
| `underparts_color` | `pink` | 4 | 0.3% | 3 |
| `upperparts_color` | `gray_brown` | 4 | 0.3% | 3 |
| `upperparts_color` | `green` | 4 | 0.3% | 4 |
| `wingtip_color` | `black` | 4 | 0.3% | 4 |
| `tail_shape` | `fan` | 4 | 0.3% | 2 |
| `behavior` | `mimicry` | 3 | 0.2% | 2 |
| `bill_shape` | `crossed` | 3 | 0.2% | 2 |
| `back_color` | `red` | 3 | 0.2% | 2 |
| `bill_color` | `blue` | 3 | 0.2% | 2 |
| `body_color` | `blue` | 3 | 0.2% | 3 |
| `body_color` | `gray_brown` | 3 | 0.2% | 3 |
| `breast_color` | `pink` | 3 | 0.2% | 2 |
| `crown_color` | `blue` | 3 | 0.2% | 3 |
| `face_color` | `red` | 3 | 0.2% | 3 |
| `nape_color` | `gold` | 3 | 0.2% | 1 |
| `nape_color` | `gray` | 3 | 0.2% | 1 |
| `plumage_color` | `cinnamon` | 3 | 0.2% | 2 |
| `plumage_color` | `gold` | 3 | 0.2% | 3 |
| `tail_color` | `rust` | 3 | 0.2% | 1 |
| `throat_color` | `pink` | 3 | 0.2% | 1 |
| `underparts_color` | `gray` | 3 | 0.2% | 2 |
| `upperparts_color` | `olive` | 3 | 0.2% | 3 |
| `back_color` | `olive` | 2 | 0.2% | 2 |
| `back_color` | `rust` | 2 | 0.2% | 2 |
| `body_color` | `blue_gray` | 2 | 0.2% | 2 |
| `cheek_color` | `black` | 2 | 0.2% | 1 |
| `cheek_color` | `blue` | 2 | 0.2% | 1 |
| `cheek_color` | `chestnut` | 2 | 0.2% | 1 |
| `chin_color` | `black` | 2 | 0.2% | 1 |
| `collar_color` | `white` | 2 | 0.2% | 2 |
| `crown_color` | `gray` | 2 | 0.2% | 2 |
| `crown_color` | `rust` | 2 | 0.2% | 1 |
| `foot_color` | `yellow` | 2 | 0.2% | 1 |
| `head_color` | `blue_gray` | 2 | 0.2% | 2 |
| `head_color` | `brown` | 2 | 0.2% | 2 |
| `nape_color` | `brown` | 2 | 0.2% | 1 |
| `neck_color` | `black` | 2 | 0.2% | 2 |
| `plumage_color` | `buff` | 2 | 0.2% | 2 |
| `rump_color` | `yellow` | 2 | 0.2% | 1 |
| `side_color` | `white` | 2 | 0.2% | 1 |
| `tail_color` | `blue` | 2 | 0.2% | 1 |
| `tail_color` | `brown` | 2 | 0.2% | 2 |
| `throat_color` | `orange` | 2 | 0.2% | 1 |
| `underparts_color` | `brown` | 2 | 0.2% | 2 |
| `wing_color` | `green` | 2 | 0.2% | 1 |
| `wingtip_color` | `gray` | 2 | 0.2% | 1 |
| `feeding_behavior` | `fishing` | 2 | 0.2% | 1 |
| `habitat_preference` | `grassland` | 2 | 0.2% | 2 |
| `habitat_preference` | `marine` | 2 | 0.2% | 2 |
| `habitat_preference` | `woodland` | 2 | 0.2% | 2 |
| `activity_period` | `crepuscular` | 1 | 0.1% | 1 |
| `back_color` | `bronze` | 1 | 0.1% | 1 |
| `back_color` | `chestnut` | 1 | 0.1% | 1 |
| `back_color` | `gold` | 1 | 0.1% | 1 |
| `bill_color` | `blue_gray` | 1 | 0.1% | 1 |
| `bill_color` | `pink` | 1 | 0.1% | 1 |
| `body_color` | `chestnut` | 1 | 0.1% | 1 |
| `body_color` | `cinnamon` | 1 | 0.1% | 1 |
| `body_color` | `green` | 1 | 0.1% | 1 |
| `body_color` | `purple` | 1 | 0.1% | 1 |
| `body_color` | `rust` | 1 | 0.1% | 1 |
| `breast_color` | `gray_brown` | 1 | 0.1% | 1 |
| `breast_color` | `purple` | 1 | 0.1% | 1 |
| `breast_color` | `yellow` | 1 | 0.1% | 1 |
| `cap_color` | `brown` | 1 | 0.1% | 1 |
| `cap_color` | `white` | 1 | 0.1% | 1 |
| `cap_color` | `yellow` | 1 | 0.1% | 1 |
| `chest_color` | `brown` | 1 | 0.1% | 1 |
| `chest_color` | `red` | 1 | 0.1% | 1 |
| `chest_color` | `white` | 1 | 0.1% | 1 |
| `chest_color` | `yellow` | 1 | 0.1% | 1 |
| `collar_color` | `chestnut` | 1 | 0.1% | 1 |
| `collar_color` | `red` | 1 | 0.1% | 1 |
| `collar_color` | `rufous` | 1 | 0.1% | 1 |
| `crest_color` | `gold` | 1 | 0.1% | 1 |
| `crest_color` | `orange` | 1 | 0.1% | 1 |
| `crest_color` | `white` | 1 | 0.1% | 1 |
| `crest_color` | `yellow` | 1 | 0.1% | 1 |
| `crown_color` | `chestnut` | 1 | 0.1% | 1 |
| `crown_color` | `green` | 1 | 0.1% | 1 |
| `crown_color` | `purple` | 1 | 0.1% | 1 |
| `eye_color` | `black` | 1 | 0.1% | 1 |
| `eye_color` | `gold` | 1 | 0.1% | 1 |
| `eye_color` | `gray` | 1 | 0.1% | 1 |
| `face_color` | `gray` | 1 | 0.1% | 1 |
| `foot_color` | `blue` | 1 | 0.1% | 1 |
| `head_color` | `chestnut` | 1 | 0.1% | 1 |
| `head_color` | `gold` | 1 | 0.1% | 1 |
| `head_color` | `orange` | 1 | 0.1% | 1 |
| `head_color` | `rust` | 1 | 0.1% | 1 |
| `nape_color` | `red` | 1 | 0.1% | 1 |
| `neck_color` | `orange` | 1 | 0.1% | 1 |
| `neck_color` | `rust` | 1 | 0.1% | 1 |
| `plumage_color` | `olive` | 1 | 0.1% | 1 |
| `rump_color` | `blue` | 1 | 0.1% | 1 |
| `rump_color` | `purple` | 1 | 0.1% | 1 |
| `shoulder_color` | `brown` | 1 | 0.1% | 1 |
| `shoulder_color` | `yellow` | 1 | 0.1% | 1 |
| `tail_color` | `rufous` | 1 | 0.1% | 1 |
| `tail_color` | `yellow` | 1 | 0.1% | 1 |
| `underparts_color` | `blue_gray` | 1 | 0.1% | 1 |
| `underparts_color` | `rufous` | 1 | 0.1% | 1 |
| `underwing_color` | `gold` | 1 | 0.1% | 1 |
| `underwing_color` | `yellow` | 1 | 0.1% | 1 |
| `upperparts_color` | `gray` | 1 | 0.1% | 1 |
| `wing_color` | `blue` | 1 | 0.1% | 1 |
| `wing_color` | `orange` | 1 | 0.1% | 1 |
| `flight_style` | `gliding` | 1 | 0.1% | 1 |
| `size` | `tiny` | 1 | 0.1% | 1 |

## Reproduce

```bash
python3 extract_description_features.py --report
```

Output: `outputs/Birdsoftheworld-features.csv`; this report is written to `outputs/description-feature-analysis.md`. Columns are generated from features observed in the input and sorted alphabetically, so a different input may produce a different set of columns. No vocabulary or ontology URIs are assigned yet; the column names are candidate concepts for later mapping.
