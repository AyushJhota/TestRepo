# Jyada Sahi Vala 
import cv2
from pyzbar.pyzbar import decode
import time

def decode_ticket_code(ticket_code, ticket_database):
    # Check if the ticket code exists in the database
    if ticket_code in ticket_database:
        return ticket_database[ticket_code]
    else:
        return None

# Example ticket database mapping ticket codes to UPI IDs
ticket_database = {
    "370c": "bheru",
    "10f6": "shubham",
    "7d29": "aj",
    "1cdd": "dines",
    "123": "123"
    # Add more entries as needed
}

# Define authorized UPI IDs for entry
authorized_upi_ids = ["bheru", "shubham", "aj","dines","123"]

# Function to read QR code from a frame
def read_qr_code(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Use pyzbar to decode QR code
    qr_codes = decode(gray)
    if qr_codes:
        # Extract ticket code from QR code data
        ticket_code = qr_codes[0].data.decode()
        return ticket_code
    else:
        return None

# Initialize video capture from Iriun Webcam
cap = cv2.VideoCapture(0)

# Variable to track time of last QR code detection
last_detection_time = 0

# Delay between processing consecutive frames (in seconds)
detection_delay = 3

# Loop to continuously capture frames from the camera
while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error reading frame from camera")
        break

    # Check if it's time to process a new frame
    if time.time() - last_detection_time >= detection_delay:
        # Attempt to read QR code from the frame
        ticket_code = read_qr_code(frame)
        if ticket_code:
            print("Ticket Code:", ticket_code)
            upi_id = decode_ticket_code(ticket_code, ticket_database)
            if upi_id:
                print("Decoded UPI ID:", upi_id)
                # Check if the UPI ID is authorized for entry
                if upi_id in authorized_upi_ids:
                    print("Allow entry")
                else:
                    print("Deny entry: UPI ID not authorized")
            else:
                print("Ticket code not found in the database")
            # Update time of last detection
            last_detection_time = time.time()

# Release camera
cap.release()















# thoda Bohot Sahi vala

# import cv2
# from pyzbar.pyzbar import decode

# def decode_ticket_code(ticket_code, ticket_database):
#     # Check if the ticket code exists in the database
#     if ticket_code in ticket_database:
#         return ticket_database[ticket_code]
#     else:
#         return None

# # Example ticket database mapping ticket codes to UPI IDs
# ticket_database = {
#     "370c": "bheru",
#     "10f6": "shubham",
#     "7d29": "aj",
#     "1cdd": "dines",
#     # Add more entries as needed
# }

# # Define authorized UPI IDs for entry
# authorized_upi_ids = ["bheru", "shubham", "aj","dines"]

# # Function to read QR code from a frame
# def read_qr_code(frame):
#     # Convert frame to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     # Use pyzbar to decode QR code
#     qr_codes = decode(gray)
#     if qr_codes:
#         # Extract ticket code from QR code data
#         ticket_code = qr_codes[0].data.decode()
#         return ticket_code
#     else:
#         return None

# # Initialize video capture from Iriun Webcam
# cap = cv2.VideoCapture(0)

# # Loop to continuously capture frames from the camera
# while True:
#     # Read a frame from the camera
#     ret, frame = cap.read()
#     if not ret:
#         print("Error reading frame from camera")
#         break

#     # Attempt to read QR code from the frame
#     ticket_code = read_qr_code(frame)
#     if ticket_code:
#         print("Ticket Code:", ticket_code)
#         upi_id = decode_ticket_code(ticket_code, ticket_database)
#         if upi_id:
#             print("Decoded UPI ID:", upi_id)
#             # Check if the UPI ID is authorized for entry
#             if upi_id in authorized_upi_ids:
#                 print("Allow entry")
#             else:
#                 print("Deny entry: UPI ID not authorized")
#         else:
#             print("Ticket code not found in the database")

# # Release camera
# cap.release()




