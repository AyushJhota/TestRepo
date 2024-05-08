
# def update_excel(data, excel_file):
#     print("Updating Excel file...")
#     df = pd.read_excel(excel_file)

#     # Check if "Scanned" column exists, if not, create it
#     if "Scanned" not in df.columns:
#         print("Adding 'Scanned' column to DataFrame...")
#         df["Scanned"] = ""

#     # Convert the data to string for consistency
#     data = str(data)

#     # Update the "Scanned" column for the corresponding ticket code
#     idx_list = df.index[df["Ticket Code"].astype(str) == data].tolist()
#     if idx_list:
#         print("Ticket code found in Excel file.")
#         idx = idx_list[0]
#         df.at[idx, "Scanned"] = "Yes"
#         df.to_excel(excel_file, index=False)
#         print("Excel file updated.")
#     else:
#         print("Ticket code not found in Excel file.")
