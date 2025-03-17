import csv
import os

def update_concept_streams():
    # Read concept progression data
    concept_progression_path = 'data/concept_progession.csv'

    # Find the highest version of problems.csv
    version = 0
    while os.path.exists(f'data/problems_v{version+1}.csv'):
        version += 1

    problems_path = f'data/problems_v{version}.csv' if version > 0 else 'data/problems.csv'

    # Determine the version number for the new file
    version = 1
    while os.path.exists(f'data/problems_v{version}.csv'):
        version += 1

    output_path = f'data/problems_v{version}.csv'

    # Read concept progression data
    concept_map = {}
    with open(concept_progression_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 3:  # Ensure row has enough columns
                problem_id = row[0].strip()
                
                
                concepts = row[-1].strip()  # Take the last column (always the latest data)
                concept_map[problem_id] = concepts
    # Read problems data and update concepts
    updated_rows = []
    with open(problems_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 4:  # Ensure row has enough columns
                problem_id = row[0].strip('"')
                if problem_id in concept_map:
                    # Replace the concepts field (index 2) with the new concepts
                    row[2] = concept_map[problem_id]
                updated_rows.append(row)

    # Write updated data to new file
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(updated_rows)
    # Update the version number in the output file
    print(f"Updated concept streams saved to {output_path}")

if __name__ == "__main__":
    update_concept_streams()
