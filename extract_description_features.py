"""Extract explicitly stated, ontology-ready traits from bird descriptions.

Run from any directory:
    python3 extract_description_features.py
    python3 extract_description_features.py --report

No external dependencies. This is a conservative, rule-based extraction, not a
species identification model: missing values mean unmentioned, not absent.
Multi-valued traits use | within a single cell (e.g. plumage_color=black|white).
"""

import argparse
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUTS = HERE / "outputs"
DEFAULT_INPUT = OUTPUTS / "Birdsoftheworld-preprocessed.csv"
DEFAULT_OUTPUT = OUTPUTS / "Birdsoftheworld-features.csv"
DEFAULT_REPORT = OUTPUTS / "description-feature-analysis.md"

# Normalize modifiers to the underlying shade; retain gray/brown and blue/gray
# blends as named shades rather than asserting either component alone.
HUES = {
    "black": "black",
    "white": "white",
    "whitish": "white",
    "brown": "brown",
    "brownish": "brown",
    "gray": "gray",
    "grey": "gray",
    "grayish": "gray",
    "greyish": "gray",
    "red": "red",
    "reddish": "red",
    "ruby": "red",
    "crimson": "red",
    "scarlet": "red",
    "orange": "orange",
    "yellow": "yellow",
    "yellowish": "yellow",
    "green": "green",
    "greenish": "green",
    "blue": "blue",
    "bluish": "blue",
    "cerulean": "blue",
    "turquoise": "blue",
    "pink": "pink",
    "pinkish": "pink",
    "purple": "purple",
    "purplish": "purple",
    "violet": "purple",
    "lilac": "purple",
    "chestnut": "chestnut",
    "rufous": "rufous",
    "rusty": "rust",
    "golden": "gold",
    "gold": "gold",
    "copper": "copper",
    "cinnamon": "cinnamon",
    "olive": "olive",
    "bronzy": "bronze",
    "buff": "buff",
    "rose": "pink",
}
# Longer alternatives first to prevent partial matches (e.g. black-and-white).
COLOR_WORD = "(?:" + "|".join(sorted(HUES, key=len, reverse=True)) + ")"
COLOR_UNIT = rf"{COLOR_WORD}(?:-(?:{COLOR_WORD}|colored))?"
COLOR_LIST = rf"{COLOR_UNIT}(?:(?:\s*(?:,|and|or|&)\s*|-and-|-){COLOR_UNIT})*"
# Explicitly list valid region phrases; avoid interpreting species names as colors.
REGIONS = {
    "plumage": "plumage",
    "feathers": "plumage",
    "feather": "plumage",
    "bird": "plumage",
    "owl": "plumage",
    "parrot": "plumage",
    "warbler": "plumage",
    "finch": "plumage",
    "body": "body",
    "head": "head",
    "crown": "crown",
    "cap": "cap",
    "throat": "throat",
    "breast": "breast",
    "chest": "chest",
    "belly": "underparts",
    "underbody": "underparts",
    "underparts": "underparts",
    "underside": "underparts",
    "upper body": "upperparts",
    "upperparts": "upperparts",
    "back": "back",
    "wing": "wing",
    "wings": "wing",
    "wingtips": "wingtip",
    "wingtip": "wingtip",
    "forewing": "wing",
    "tail": "tail",
    "bill": "bill",
    "beak": "bill",
    "leg": "leg",
    "legs": "leg",
    "foot": "foot",
    "feet": "foot",
    "eye": "eye",
    "eyes": "eye",
    "neck": "neck",
    "face": "face",
    "cheek": "cheek",
    "cheeks": "cheek",
    "shoulder": "shoulder",
    "rump": "rump",
    "nape": "nape",
    "crest": "crest",
    "collar": "collar",
    "chin": "chin",
    "sides": "side",
    "side": "side",
    "underwing": "underwing",
}
REGION_WORD = (
    "(?:" + "|".join(re.escape(s) for s in sorted(REGIONS, key=len, reverse=True)) + ")"
)
# Allow color + pattern words + region, including "yellow throat patch" and
# "white stripes on its face". Limit intervening words to avoid clause bleed.
COLOR_BEFORE_REGION = re.compile(
    rf"\b(?P<colors>{COLOR_LIST})(?:\s+|-(?:tipped|streaked)\s+|-)(?:(?:mottled|streaked|striped|barred|spotted|checkered|patterned|patch(?:es)?|stripes?|bars?|ring|band|tips?|feathers|plumage|facial|wing)\s+){{0,2}}(?P<region>{REGION_WORD})\b",
    re.IGNORECASE,
)
COLOR_PATCH_ON_REGION = re.compile(
    rf"\b(?P<colors>{COLOR_LIST})\s+(?:patch(?:es)?|spot|spots|stripes?|bars?)\s+(?:on|across|of)\s+(?:its\s+|the\s+)?(?P<region>{REGION_WORD})\b",
    re.IGNORECASE,
)
# Color enumerations following "plumage, including ..." have no region after
# the individual color words. Stop at the next full trait (", a ...").
PLUMAGE_LIST = re.compile(
    r"\bplumage,?\s+(?:including|featuring)\s+(.*?)(?=,\s+(?:a|an|the)\s+|$)",
    re.IGNORECASE,
)


TRAITS = {
    "appearance_iridescent": r"\b(?:iridescent|metallic sheen|shimmering)\b",
    "plumage_pattern_mottled": r"\bmottled\b",
    "plumage_pattern_streaked": r"\b(?:streaked|streaks)\b",
    "plumage_pattern_striped": r"\b(?:striped|stripes)\b",
    "plumage_pattern_barred": r"\b(?:barred|bars)\b",
    "plumage_pattern_spotted": r"\b(?:spotted|spots)\b",
    "head_crest": r"\b(?:crest(?:ed)?|topknot)\b",
    "head_ear_tufts": r"\bear tufts?\b",
    "head_mask": r"\b(?:facial\s+)?mask\b",
    "head_eye_ring": r"\beye[- ]ring\b",
    "bill_shape_hooked": r"\bhooked\s+(?:bill|beak)\b",
    "bill_shape_spoon": r"\bspoon-shaped\s+(?:bill|beak)\b",
    "bill_shape_crossed": r"\bcrossed\s+(?:bill|beak)\b",
    "bill_shape_upturned": r"\b(?:upturned|upward-curv(?:ed|ing))\s+(?:bill|beak)\b",
    "bill_shape_downcurved": r"\bdownward-curv(?:ed|ing)\s+(?:bill|beak)\b",
    "bill_shape_curved": r"(?<!-)\bcurved\s+(?:bill|beak)\b",
    "bill_shape_dagger": r"\bdagger-like\s+(?:bill|beak)\b",
    "bill_length_long": r"\blong(?:er)?(?:,\s*(?:thin|slender))?\s+(?:bill|beak)\b",
    "bill_length_short": r"\b(?:short|small)\s+(?:bill|beak)\b",
    "bill_shape_slender": r"\b(?:slender|thin)(?:,?\s+(?:red|black|yellow|white|long))?\s+(?:bill|beak)\b",
    "tail_shape_forked": r"\b(?:deeply\s+)?forked\s+tail\b",
    "tail_shape_fan": r"\bfan-shaped\s+tail\b",
    "tail_length_long": r"\blong(?:,\s*(?:pointed|tapered))?\s+tail\b",
    "neck_length_long": r"\blong(?:,\s*slender)?\s+neck\b",
    "leg_length_long": r"\blong\s+(?:(?:pink|black|red|gray)\s+)?legs\b",
    "legs_feathered": r"\bfeathered\s+(?:legs|feet)\b",
    "vocalization_call": r"\b(?:call|calls)\b",
    "vocalization_song": r"\b(?:song|singing|trill|trilling)\b",
    "activity_nocturnal": r"\bnocturnal\b",
    "activity_crepuscular": r"\bcrepuscular\b",
    "locomotion_wading": r"\bwading\b",
    "locomotion_diving": r"\bdiving\b",
    "flight_hovering": r"\bhovering\b",
    "flight_soaring": r"\bsoaring\b",
    "flight_gliding": r"\bgliding\b",
    "diet_fishing": r"\bfish(?:ing)?\b",
    "behavior_scavenging": r"\bscavenging\b",
    "behavior_mimicry": r"\bmimicry\b",
    "behavior_courtship_display": r"\b(?:courtship|display dance)\b",
    "habitat_coastal": r"\b(?:coastal|beaches|shores|estuar(?:y|ies))\b",
    "habitat_wetland": r"\b(?:wetlands?|marsh(?:y|es)?|mudflats?)\b",
    "habitat_freshwater": r"\b(?:freshwater|ponds?|lakes?)\b",
    "habitat_grassland": r"\bgrasslands?\b",
    "habitat_woodland": r"\bwood(?:ed|lands?)\b",
    "habitat_marine": r"\bmarine\b",
}
TRAIT_PATTERNS = {k: re.compile(v, re.IGNORECASE) for k, v in TRAITS.items()}
SIZE = re.compile(r"\b(tiny|small|medium-sized|large)\b", re.IGNORECASE)


def hues(text):
    """Map literal color expression to one or more standardized color labels."""
    result = set()
    for raw in re.findall(COLOR_WORD, text.lower()):
        result.add(HUES[raw])
    # Keep named mixed shades distinct; do not conflate grayish-brown with
    # an unqualified gray or brown bird.
    for match in re.finditer(
        r"\b(?:grayish-brown|brownish-gray|gray-brown|grey-brown)\b",
        text,
        re.IGNORECASE,
    ):
        result.difference_update({"gray", "brown"})
        result.add("gray_brown")
    for match in re.finditer(
        r"\b(?:blue-gray|bluish-gray|grayish-blue)\b", text, re.IGNORECASE
    ):
        result.difference_update({"blue", "gray"})
        result.add("blue_gray")
    return result


def extract(description):
    """Return a set of positive, explicitly mentioned atomic feature names."""
    text = description.lower()
    features = set()
    size = SIZE.search(text)
    if size:
        features.add(
            "size_" + ("medium" if size.group() == "medium-sized" else size.group())
        )
    if re.search(r"\btall\b", text):
        features.add("height_tall")
    for name, pattern in TRAIT_PATTERNS.items():
        if pattern.search(text):
            features.add(name)
    for pattern in (COLOR_BEFORE_REGION, COLOR_PATCH_ON_REGION):
        for match in pattern.finditer(text):
            region = REGIONS[match.group("region")]
            for hue in hues(match.group("colors")):
                features.add(f"color_{region}_{hue}")
    for match in PLUMAGE_LIST.finditer(text):
        for hue in hues(match.group(1)):
            features.add(f"color_plumage_{hue}")
    return features


def feature_slot(feature):
    """Translate a detected value into its categorical column and normalized value."""
    if feature.startswith("color_"):
        suffix = feature.removeprefix("color_")
        for region in sorted(set(REGIONS.values()), key=len, reverse=True):
            if suffix.startswith(region + "_"):
                return f"{region}_color", suffix[len(region) + 1 :]
        raise ValueError(f"Unrecognized color region: {feature}")
    special = {
        "head_crest": ("head_ornament", "crest"),
        "head_ear_tufts": ("head_ornament", "ear_tufts"),
        "head_mask": ("head_marking", "mask"),
        "head_eye_ring": ("head_marking", "eye_ring"),
        "legs_feathered": ("leg_covering", "feathered"),
        "appearance_iridescent": ("plumage_finish", "iridescent"),
        "diet_fishing": ("feeding_behavior", "fishing"),
        "height_tall": ("height", "tall"),
    }
    if feature in special:
        return special[feature]
    for prefix, column in (
        ("plumage_pattern_", "plumage_pattern"),
        ("bill_shape_", "bill_shape"),
        ("bill_length_", "bill_length"),
        ("tail_shape_", "tail_shape"),
        ("tail_length_", "tail_length"),
        ("neck_length_", "neck_length"),
        ("leg_length_", "leg_length"),
        ("vocalization_", "vocalization"),
        ("activity_", "activity_period"),
        ("locomotion_", "locomotion"),
        ("flight_", "flight_style"),
        ("behavior_", "behavior"),
        ("habitat_", "habitat_preference"),
        ("size_", "size"),
    ):
        if feature.startswith(prefix):
            return column, feature[len(prefix) :]
    raise ValueError(f"Unrecognized extracted trait: {feature}")


def categorical_values(features):
    """Group independent values by trait; sort multivalued cells deterministically."""
    values = defaultdict(set)
    for feature in features:
        column, value = feature_slot(feature)
        values[column].add(value)
    return {column: "|".join(sorted(found)) for column, found in values.items()}


def report_text(
    rows, feature_sets, columns, source_name="outputs/Birdsoftheworld-preprocessed.csv"
):
    n = len(rows)
    species = {row["species"] for row in rows}
    counts = Counter(f for features in feature_sets for f in features)
    distinct_species = defaultdict(set)
    for row, features in zip(rows, feature_sets):
        for feature in features:
            distinct_species[feature].add(row["species"])
    ordered = sorted(counts, key=lambda f: (-counts[f], f))

    def table_row(feature):
        column, value = feature_slot(feature)
        return (
            f"| `{column}` | `{value}` | {counts[feature]} | "
            f"{counts[feature] / n:.1%} | {len(distinct_species[feature])} |"
        )

    lines = [
        "# Bird description feature analysis",
        "",
        (
            f"Source: `{source_name}` ({n:,} rows, {len(species):,} species; "
            f"{sum(bool(r['description of bird'].strip()) for r in rows):,} nonempty descriptions)."
        ),
        "",
        "## Method",
        "",
        (
            "Counts below are **rows with an explicit textual mention**, not biological prevalence. "
            "A description can mention multiple colors/traits; columns are non-exclusive. "
            "Color is bound to its named body part (e.g. `head_color=white`), while "
            "`plumage_color=white` is reserved for explicitly general plumage/feather wording. "
            "Mixed gray-brown and blue-gray are kept as separate named shades; "
            "black-and-white is split into black and white. Ruby-red/crimson map to red; "
            "spelling variants and plurals are normalized. Each feature column holds its "
            "value (e.g. `size=small`); explicit multiple values are sorted and joined "
            "with `|` (e.g. `plumage_color=black|white`). A blank means unmentioned "
            "(unknown, **not false**), and `|` is not part of any individual value. "
            "The original description and other input columns are retained."
        ),
        "",
        (
            "Rules are intentionally conservative and do not infer traits from the species, "
            "the separate `feather color` column, or a habitat inferred from a bird group. "
            "They do not resolve negation, uncertainty, or every possible paraphrase. "
            "Check the original description before linking traits to ontologies; "
            "a different source row is not an independent observation of a species."
        ),
        "",
        (
            f"Categorical columns: **{len(columns)}**; distinct observed column/value "
            f"pairs: **{len(counts)}**. Rows with at least one feature: "
            f"**{sum(bool(f) for f in feature_sets):,}/{n:,}**. "
            "The species count measures how broadly a feature is mentioned across "
            "distinct species; low species counts can indicate distinctive wording "
            "but do not establish biological uniqueness."
        ),
        "",
        "## Most frequently mentioned atomic values",
        "",
        "| Column | Value | Rows | % rows | Species |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for f in ordered[:30]:
        lines.append(table_row(f))
    lines.extend(
        [
            "",
            "## Repeated but relatively concentrated mentions",
            "",
            (
                "Traits mentioned in at least 10 rows but across at most 10 species, "
                "ranked by row count. Repeated descriptions can inflate row counts; "
                "these are leads for review, not measures of species specificity."
            ),
            "",
            "| Column | Value | Rows | % rows | Species |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    concentrated = [
        f for f in ordered if counts[f] >= 10 and len(distinct_species[f]) <= 10
    ]
    for f in concentrated[:15]:
        lines.append(table_row(f))
    lines.extend(
        [
            "",
            "## Less common, potentially distinguishing traits",
            "",
            (
                "Examples with at least two mentions, ranked by fewest species then most rows; "
                "rarity in this dataset is not proof of diagnostic value."
            ),
            "",
            "| Column | Value | Rows | % rows | Species |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    candidates = [f for f in counts if counts[f] >= 2 and not f.startswith("size_")]
    candidates.sort(key=lambda f: (len(distinct_species[f]), -counts[f], f))
    for f in candidates[:20]:
        lines.append(table_row(f))
    lines.extend(
        [
            "",
            "## Complete column/value inventory",
            "",
            (
                "These are all observed values within the categorical columns. "
                "Counts include duplicate descriptions/rows; `Species` deduplicates species names."
            ),
            "",
            "| Column | Value | Rows | % rows | Species |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for f in ordered:
        lines.append(table_row(f))
    lines.extend(
        [
            "",
            "## Reproduce",
            "",
            "```bash",
            "python3 extract_description_features.py --report",
            "```",
            "",
            (
                "Output: `outputs/Birdsoftheworld-features.csv`; this report is written "
                "to `outputs/description-feature-analysis.md`. Columns are generated from "
                "features observed in the input and sorted alphabetically, so a "
                "different input may produce a different set of columns. "
                "No vocabulary or ontology URIs are assigned yet; the column names "
                "are candidate concepts for later mapping."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--report",
        nargs="?",
        type=Path,
        const=DEFAULT_REPORT,
        help="write a Markdown analysis (default: outputs/description-feature-analysis.md)",
    )
    args = parser.parse_args()
    with args.input.open(newline="", encoding="utf-8-sig") as infile:
        reader = csv.DictReader(infile)
        if (
            not reader.fieldnames
            or "description of bird" not in reader.fieldnames
            or "species" not in reader.fieldnames
        ):
            parser.error("input must have 'species' and 'description of bird' headers")
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    features = [extract(row["description of bird"] or "") for row in rows]
    columns = sorted({feature_slot(f)[0] for found in features for f in found})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames + columns)
        writer.writeheader()
        for row, found in zip(rows, features):
            writer.writerow({**row, **categorical_values(found)})
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        source = (
            str(args.input.relative_to(HERE))
            if args.input.is_relative_to(HERE)
            else str(args.input)
        )
        args.report.write_text(
            report_text(rows, features, columns, source), encoding="utf-8"
        )
    print(f"{len(rows)} rows, {len(columns)} categorical columns -> {args.output}")


if __name__ == "__main__":
    main()
