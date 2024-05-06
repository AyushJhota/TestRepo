import hashlib
import qrcode
import pandas as pd
import os.path

def generate_ticket_code(upi_id):
    # Hash the UPI ID using SHA-256 algorithm to create a unique ticket code
    hashed_id = hashlib.sha256(upi_id.encode()).hexdigest()
    # Take a portion of the hashed ID as the ticket code
    ticket_code = hashed_id[:16]  # Fixed-length ticket code
    return ticket_code

def generate_qr_code(data, filename):
    # Generate QR code with the provided data
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="gold")

    # Save the image to a file
    img.save(filename)

def save_to_excel(name, upi_id, ticket_code, excel_file):
    # Create or load the Excel file
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
    else:
        df = pd.DataFrame(columns=["Name", "UPI ID", "Ticket Code"])

    # Check for duplicate names
    if (df["Name"] == name).any():
        print("QR code with the same name already exists. Skipping...")
        return

    # Check if the UPI ID already exists
    if (df["UPI ID"] == upi_id).any():
        print("QR code with the same UPI ID already exists. Skipping...")
        return

    # Check if the ticket code already exists
    if (df["Ticket Code"] == ticket_code).any():
        print("QR code with the same ticket code already exists. Skipping...")
        return

    # Append the new data to the DataFrame
    new_entry = pd.DataFrame({"Name": [name], "UPI ID": [upi_id], "Ticket Code": [ticket_code]})
    df = pd.concat([df, new_entry], ignore_index=True)

    # Save the DataFrame to the Excel file
    df.to_excel(excel_file, index=False)

    # Generate QR code only if the entry is successfully appended
    qr_code_filename = f"{name}.png"
    generate_qr_code(ticket_code, qr_code_filename)

    print("Data saved to:", excel_file)



# Example usage:
upi_id = input("Enter Upi id:")
ticket_code = generate_ticket_code(upi_id)
print("Ticket Code:", ticket_code)

# Prompt for the name of the QR code file
name = input("Enter name for the QR code file: ")
qr_code_filename = f"{name}.png"

# Generate QR code for the ticket code with the specified name
generate_qr_code(ticket_code, qr_code_filename)

# Save the data to an Excel file with the specified name
excel_file = "ticket_data.xlsx"
save_to_excel(name, upi_id, ticket_code, excel_file)
