import csv

input_file = 'Birdsoftheworld.csv'
output_file = 'Birdsoftheworld-fixed.csv'

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    
    writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
    
    for i, line in enumerate(infile):
        # Strip invisible characters and trailing commas from the end of the line
        line = line.strip('\n\r, ')
        parts = line.split(',')
        
        # Explicitly write the 6 known headers for the first row
        if i == 0:
            writer.writerow(['species', 'location', 'time', 'description of bird', 'sex', 'feather color'])
            continue
            
        # Recombine fragmented descriptions for rows with rogue commas
        if len(parts) > 6:
            species = parts[0]
            location = parts[1]
            time = parts[2]
            feather_color = parts[-1]
            sex = parts[-2]
            description = ",".join(parts[3:-2])
            writer.writerow([species, location, time, description, sex, feather_color])
            
        # Write standard rows exactly as they are
        elif len(parts) == 6:
            writer.writerow(parts)
            
        # Pad rows that might be missing data at the end to ensure 6 columns
        else:
            parts.extend([''] * (6 - len(parts)))
            writer.writerow(parts)