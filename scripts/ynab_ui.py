import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os

class CSVConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title('CSV Converter')
        self.root.geometry('400x200')

        # Frame for buttons
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        # Button to select the input CSV file
        self.file_path_var = tk.StringVar()
        tk.Button(frame, text="Select CSV File", command=self.select_file).pack(fill=tk.X)

        # Label to display selected file path
        self.file_label = tk.Label(frame, textvariable=self.file_path_var, fg="blue")
        self.file_label.pack(pady=10)

        # Button to perform conversion
        tk.Button(frame, text="Convert File", command=self.convert_file).pack(fill=tk.X)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.file_path_var.set(file_path)

    def convert_csv_format(self, input_file_path):
        base = os.path.splitext(input_file_path)[0]
        output_file_path = f"{base}_converted.csv"

        with open(input_file_path, mode='r', encoding='utf-8') as infile, \
            open(output_file_path, mode='w', encoding='utf-8', newline='') as outfile:
            
            reader = csv.DictReader(infile)
            fieldnames = ["Date", "Payee", "Memo", "Outflow", "Inflow"]
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for row in reader:
                memo = row['Account number']
                amount_eur = float(row['Amount (EUR)'].replace('-', '')) if row['Amount (EUR)'] != "-" else 0.0
                outflow = amount_eur if row['Transaction type'] != "Income" else ""
                inflow = amount_eur if row['Transaction type'] == "Income" else ""
                
                new_row = {
                    "Date": row["Date"],
                    "Payee": row["Payee"],
                    "Memo": memo,
                    "Outflow": outflow,
                    "Inflow": inflow,
                }
                writer.writerow(new_row)
        return output_file_path

    def convert_file(self):
        if not self.file_path_var.get():
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        output_file_path = self.convert_csv_format(self.file_path_var.get())
        messagebox.showinfo("Success", f"File converted successfully:\n{output_file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVConverterApp(root)
    root.mainloop()
