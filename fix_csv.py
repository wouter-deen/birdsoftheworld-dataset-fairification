import csv

# Replace with your actual file names
input_file = 'Birdsoftheworld.csv' 
output_file = 'bird_sightings_fixed.csv'

# The anchor values we will look for to identify the sex column
valid_sexes = ['Male', 'Female', 'Unknown']

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:
     
    # Using quoting ensures that internal commas don't break the CSV structure again
    writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['species', 'location', 'time', 'description of bird', 'sex', 'feather color'])
    
    lines = infile.readlines()
    for line in lines[1:]: # Skip the original header
        line = line.strip()
        if not line: 
            continue
        
        parts = [p.strip() for p in line.split(',')]
        
        # The first three columns never contain commas and are safe
        species = parts[0]
        location = parts[1]
        time = parts[2]
        
        # The rest of the list contains the description, sex, and colour mixed together
        remaining = parts[3:]
        
        # Search backwards through the remaining parts to find the index of the sex value
        sex_index = -1
        for i in range(len(remaining)-1, -1, -1):
            if remaining[i].capitalize() in valid_sexes:
                sex_index = i
                break
                
        if sex_index != -1:
            # Rejoin everything before the anchor as the description
            description = ', '.join(remaining[:sex_index]).replace('"', '')
            # The anchor is the sex
            sex = remaining[sex_index].capitalize()
            # Rejoin everything after the anchor as the feather colour
            color = ', '.join(remaining[sex_index+1:]).replace('"', '')
        else:
            # Fallback if no valid sex is found in the row
            description = ', '.join(remaining).replace('"', '')
            sex = ""
            color = ""
            
        writer.writerow([species, location, time, description, sex, color])
