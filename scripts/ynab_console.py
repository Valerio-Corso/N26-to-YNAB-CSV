import csv
import argparse
import os

# Function to convert the CSV format based on the specified criteria
def convert_csv_format(input_file_path):
    # Generate output file path by appending "_converted" before the file extension
    base = os.path.splitext(input_file_path)[0]
    output_file_path = f"{base}_converted.csv"

    with open(input_file_path, mode='r', encoding='utf-8') as infile, \
         open(output_file_path, mode='w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = ["Date", "Payee", "Memo", "Outflow", "Inflow"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for row in reader:
            # Using Account number as Memo
            memo = row['Account number']
            amount_eur = float(row['Amount (EUR)'].replace('-', '')) if row['Amount (EUR)'] != "-" else 0.0
            # Determining Outflow and Inflow based on Transaction type
            if row['Transaction type'] == "Income":
                outflow = ""
                inflow = amount_eur
            else:
                outflow = amount_eur
                inflow = ""
            
            new_row = {
                "Date": row["Date"],
                "Payee": row["Payee"],
                "Memo": memo,
                "Outflow": outflow,
                "Inflow": inflow,
            }
            writer.writerow(new_row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a CSV file to a specified format and save it in the same folder with "_converted" appended to the filename.')
    parser.add_argument('input_file_path', type=str, help='Path to the input CSV file')

    args = parser.parse_args()

    convert_csv_format(args.input_file_path)