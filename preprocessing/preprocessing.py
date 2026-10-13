import csv
import re
from pathlib import Path

project_dir = Path(__file__).resolve().parent
input_file = project_dir / "Birdsoftheworld.csv"
output_file = project_dir / "outputs" / "Birdsoftheworld-preprocessed.csv"

# The anchor values we will look for to identify the sex column
valid_sexes = ["Male", "Female", "Unknown"]

# The LAST occurrence of a sex value in a row separates the description from the
# feather color. Mangled rows contain duplicated "...,<sex>,<color>" tails, so the
# greedy (leftmost-longest) description group is what makes this pick the real
# sex and color instead of the duplicated copy.
# A sex value can itself be wrapped in broken quoting ("Unknown,Gray"), which
# is why optional quote characters are allowed around the anchor.
tail_re = re.compile(
    r"^(?P<desc>.*),\s*[\"']*(?P<sex>Male|Female|Unknown)[\"']*\s*(?:,\s*(?P<color>.*))?$",
    re.IGNORECASE,
)

# A sex value that still appears inside the description marks the start of a
# duplicated tail; everything from that comma onward is corruption.
duplicate_re = re.compile(r",\s*[\"']*(?:Male|Female|Unknown)[\"']*\s*,", re.IGNORECASE)


# The time column always has this shape; it anchors the split between location
# and description, because locations like "Washington, D.C." can contain commas.
time_re = re.compile(r"\d{2}-\d{2}-\d{4} \d{2}:\d{2}")


def clean_text(text):
    """Repair the quoting damage the source file carries."""
    # Doubled quotes are escaped content quotes (""V"" -> "V");
    # any quote left after that is broken CSV quoting and gets dropped.
    text = text.replace('""', "\x00")
    text = text.replace('"', "")
    text = text.replace("\x00", '"')
    # Collapse whitespace runs and strip stray commas at the edges
    text = re.sub(r"\s+", " ", text)
    return text.strip().strip(",").strip()


output_file.parent.mkdir(parents=True, exist_ok=True)

with (
    open(input_file, "r", encoding="utf-8") as infile,
    open(output_file, "w", encoding="utf-8", newline="") as outfile,
):
    # Using quoting ensures that internal commas don't break the CSV structure again
    writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(
        ["species", "location", "time", "description of bird", "sex", "feather color"]
    )

    lines = infile.readlines()
    for line in lines[1:]:  # Skip the original header
        # The source rows carry a variable number of padding commas at the end
        line = line.rstrip("\r\n").rstrip(",").strip()
        if not line:
            continue

        # Species never contains a comma; the location can ("Washington, D.C."),
        # so split on the first comma and locate the timestamp to its right
        species, _, remainder = line.partition(",")
        time_match = time_re.search(remainder)
        if time_match:
            location = remainder[: time_match.start()].rstrip(",").strip()
            time = time_match.group()
            rest = remainder[time_match.end() :].lstrip(",").strip()
        else:
            # Fallback for rows without a recognisable timestamp
            parts = remainder.split(",", 2)
            location, time, rest = (parts + ["", ""])[:3]

        description = rest
        sex = ""
        color = ""

        match = tail_re.match(rest)
        if match:
            description = match.group("desc") or ""
            sex = match.group("sex").capitalize()
            color = match.group("color") or ""

        # Drop duplicated tails: cut the description at the first sex value
        # that still appears inside it, and repeat in case of more copies.
        while True:
            duplicate = duplicate_re.search(description)
            if not duplicate:
                break
            description = description[: duplicate.start()]

        description = clean_text(description)
        color = clean_text(color)

        writer.writerow([species, location, time, description, sex, color])
