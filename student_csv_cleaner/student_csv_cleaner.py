import csv

# FILE CONFIGURATION

# Name of the CSV file we want to read
INPUT_FILE = "student.csv"

# Name of the new cleaned CSV file to be created
OUTPUT_FILE = "cleaned_student.csv"

# Column names for the cleaned CSV file
HEADERS = ["Names", "Scores", "Departments"]

# ROW VALIDATION
def validate_row(row):

    # Check if the row has exactly 3 columns
    if len(row) != 3:
        return None
    
    # Remove extra spaces from the columns
    name = row[0].strip()
    score = row[1].strip()
    department = row[2].strip()

    # Empty columns are not allowed
    if not name:
        return None
    
    if not department:
        return None
    
    if not score:
        return None

    # Convert the score into a number
    try:
        score = float(score)
    except ValueError:
        return None
    
    # Ensure the score is between 0 and 100
    if score < 0 or score > 100:
        return None
    
    if score.is_integer():
        score = int(score)

    return [name, score, department]

# READ, VALIDATE AND CLEAN CSV FILE
def clean_csv():
    cleaned_rows = []
    try:
        # Open CSV file for reading
        with open(INPUT_FILE, "r", newline="") as file:
            reader = csv.reader(file)

            # Skip the first row because it contains headers
            next(reader, None)

            # Loop through every student record
            for row in reader:
                if not row or all(data.strip() == "" for data in row):
                    continue

                # Send the row to validation function
                cleaned_row = validate_row(row)

                if cleaned_row:
                    cleaned_rows.append(cleaned_row)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} does not exist.")
        return

    # Open the output file for writing
    with open(OUTPUT_FILE, "w", newline="") as file:
        
        # Create a CSV writer object
        writer = csv.writer(file)

        # Write the column headings first
        writer.writerow(HEADERS)

        # Write all the cleaned student records
        writer.writerows(cleaned_rows)
    
    # Inform the user that the process finished
    print("CSV cleaning completed successfully!")

    # Show number of valid records saved
    print(f"Cleaned records: {len(cleaned_rows)}")

    # Show the output file name
    print(f"Output file: {OUTPUT_FILE}")

# MAIN FUNCTION
def main():
    clean_csv()

if __name__ == "__main__":
    main()
