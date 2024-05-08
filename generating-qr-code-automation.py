import pandas as pd
import hashlib
import qrcode
import os

def generate_ticket_code(upi_id):
    hashed_id = hashlib.sha256(upi_id.encode()).hexdigest()
    return hashed_id[:16]

def generate_qr_code(upi_id, name, output_folder):
    ticket_code = generate_ticket_code(upi_id)
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=2,
    )
    qr.add_data(ticket_code)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_location = f"{output_folder}/{name}.png"
    qr_img.save(qr_location)
    return ticket_code, qr_location

def generate_qr_codes_from_excel(excel_file, output_folder):
    df = pd.read_excel(excel_file)
    df['Ticket Code'] = ""
    df['QR Location'] = ""
    for index, row in df.iterrows():
        upi_id = row['UPI ID']
        name = row['Name']
        ticket_code, qr_location = generate_qr_code(upi_id, name, output_folder)
        df.at[index, 'Ticket Code'] = ticket_code
        df.at[index, 'QR Location'] = qr_location
    df.to_excel(excel_file, index=False)

# Example usage
excel_file = "data.xlsx"
output_folder = "qr_codes"
generate_qr_codes_from_excel(excel_file, output_folder)
