# TestRepo


QR Code Ticket Scanner
Overview
This application is designed to facilitate the scanning and management of event tickets using QR codes. It provides a seamless way to verify ticket validity, update attendee access status, and manage event attendance.

How It Works
Generate QR Codes: Utilize the provided ticket_generator.py script to generate unique QR codes for each event attendee. These QR codes contain encrypted ticket information.
Scan QR Codes: Run the scanner.py application and point the camera towards the QR code of the attendee's ticket. The scanner captures the QR code and extracts the encoded ticket information.
Validate Tickets: The application cross-references the extracted ticket information with the attendee database stored in the data.xlsx Excel sheet. If the ticket is valid and matches an attendee, access is granted.
Update Attendance: Upon successful validation, the attendee's access status is updated in real-time. The data.xlsx Excel sheet is updated to reflect the attendee's presence at the event.
User Interface: The application provides a user-friendly interface with interactive access messages. Attendees are greeted with personalized messages upon successful validation.
Getting Started
Installation: Clone the repository and install the required dependencies using pip install -r requirements.txt.
Generate QR Codes: Use the ticket_generator.py script to generate QR codes for each attendee by providing their details in the data.xlsx Excel sheet.
Run the Scanner: Execute the scanner.py script to start the QR code scanning process. Follow the on-screen instructions to scan tickets and manage attendee access.
Directory Structure
data.xlsx: Excel sheet containing attendee information.
qr_codes/: Folder containing generated QR codes.
scanner.py: QR code scanning application.
ticket_generator.py: Script for generating QR codes from Excel.
License
This project is licensed under the MIT License - see the LICENSE file for details.