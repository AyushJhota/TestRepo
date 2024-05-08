import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import threading
import tkinter as tk

class QRCodeScanner:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.scan_thread = threading.Thread(target=self.scan_loop)
        self.stop_scan = False

    def start_scan(self):
        self.scan_thread.start()

    def stop(self):
        self.stop_scan = True

    def scan_loop(self):
        while not self.stop_scan:
            ret, frame = self.capture.read()
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                print("Decoded Data:", data)
                access_status, attendee_name = check_access(data, "ticket_data.xlsx")  # Get attendee name
                print(access_status)  # Print the access status
                show_access_message(access_status, attendee_name, data, on_next_button_click)  # Pass the decoded data
                if access_status.startswith("Welcome"):  # Check if access is granted
                    update_excel(data, "ticket_data.xlsx")  # Update excel if access is granted
                # Add any further processing here
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.waitKey(1000)  # Add a delay of (1000 = 1) seconds before scanning again

        self.capture.release()
        cv2.destroyAllWindows()


def check_access(data, excel_file):
    df = pd.read_excel(excel_file)
    if data in df.values:
        attendee_name = df.loc[df['Ticket Code'] == data, 'Name'].values[0]
        print("Grant Access!")
        return f"Welcome {attendee_name}!!!", attendee_name  # Return both welcome message and name
    else:
        print("No Entry!")
        return "Sorry the Data was not recognised.", None  # Return None if data is not recognized

def update_excel(data, excel_file):
    df = pd.read_excel(excel_file)
    idx_list = df.index[df["Ticket Code"] == data].tolist()
    if idx_list:
        idx = idx_list[0]
        df.at[idx, "Scanned"] = "Yes"
        df.to_excel(excel_file, index=False)
        print("Excel file updated.")
    else:
        print("Ticket code not found in Excel file.")

class AccessMessageWindow:
    def __init__(self, message, attendee_name, decoded_data, callback):
        self.root = tk.Tk()
        self.root.title("Ticket Tracker")
        
        # Set window size
        self.root.geometry("400x200")
        
        # Set window position on right top side
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"+{screen_width - 400}+0")
        
        # Set window background color
        self.root.config(bg="gray10")
        
        self.message_label = tk.Label(self.root, text=message, font=("Helvetica", 16), fg="white", bg="gray10")
        self.message_label.pack(pady=20)
        
        # Display the decoded data (ticket ID)
        if decoded_data:
            decoded_label = tk.Label(self.root, text=f"Ticket ID: {decoded_data}", font=("Arial", 12), fg="#666666", bg="#f0f0f0")
            decoded_label.pack(pady=5)
        
        self.next_button = tk.Button(self.root, text="Next", command=callback, bg="gray30", fg="white")
        self.next_button.pack(pady=10)

    def run(self):
        self.root.mainloop()


def show_access_message(message, attendee_name, decoded_data, callback):
    global access_window
    if message.startswith("Welcome"):
        message = f"Welcome {attendee_name}!!!"
    access_window = AccessMessageWindow(message, attendee_name, decoded_data, callback)
    access_window.run()





def on_next_button_click():
    global access_window
    access_window.root.destroy()

if __name__ == "__main__":
    scanner = QRCodeScanner()
    scanner.start_scan()




