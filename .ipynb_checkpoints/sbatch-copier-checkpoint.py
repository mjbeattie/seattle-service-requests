"""
sbatch-copier.py
June 15, 2024

This script creates copies of an sbatch file and increments the line input variables
for the script called in the sbatch file.
"""


import shutil, re

# Define the source and destination filenames
source_filename = "mjb-fifi-0.sbatch"
destination_template = "mjb-fifi-{}.sbatch"

# Loop through integers from 0 to 9
recordcount = 305971
ecordcount = 25971
blocknum = 0
startrow = 0
endrow = 5000
while endrow < recordcount:
    # Define string to replace in sbatch file
    oldstring = f"--blocknum=0 --startrow=0 --endrow=5000"
    
    blocknum += 1
    startrow = endrow
    endrow += min(5000, recordcount-endrow)

    # Provide new string for sbatch file
    newstring = f"--blocknum={blocknum} --startrow={startrow} --endrow={endrow}"

    # Create a copy of the base sbatch file
    filename = f"mjb-fifi-{blocknum}.sbatch"
    destination_filename = destination_template.format(blocknum)
    shutil.copy(source_filename, destination_filename)

    # Replace the string in the new file
    try:
        with open(destination_filename, 'r') as file:
            content = file.read()
        content = content.replace(oldstring, newstring)
        with open(destination_filename, 'w') as file:
            file.write(content)
    except FileNotFoundError:
        print(f"File {destination_filename} not found.")

print("All files copied successfully!")
