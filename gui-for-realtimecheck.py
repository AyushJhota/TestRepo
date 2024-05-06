import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import threading
import tkinter as tk
from PIL import Image, ImageTk

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
                access_status, decoded_data = check_access(data, "ticket_data.xlsx")
                print(access_status)  # Print the access status
                show_access_message(access_status, decoded_data)
                if access_status == "Welcome !!!":
                    update_excel(data, "ticket_data.xlsx")
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
        return "Welcome", attendee_name
    else:
        print("No Entry!")
        return "Sorry the Data was not recognized.", None

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
    def __init__(self, message, decoded_data):
        self.root = tk.Tk()
        self.root.title("Access Message")
        
        # Set window size
        self.root.geometry("400x200")
        
        # Set window position to the middle of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width - 400) // 2
        y_coordinate = (screen_height - 200) // 2
        self.root.geometry(f"400x200+{x_coordinate}+{y_coordinate}")
        
        # Display the access message and decoded data
        label_message = tk.Label(self.root, text=message, font=("Arial", 14))
        label_message.pack(pady=10)
        if decoded_data:
            label_data = tk.Label(self.root, text=f"Decoded Data: {decoded_data}", font=("Arial", 12))
            label_data.pack(pady=5)
        
        # Add the next button
        button_next = tk.Button(self.root, text="Next", command=self.root.destroy)
        button_next.pack(pady=10)

    def run(self):
        self.root.mainloop()

def show_access_message(message, decoded_data):
    access_window = AccessMessageWindow(message, decoded_data)
    access_window.run()

if __name__ == "__main__":
    scanner = QRCodeScanner()
    scanner.start_scan()
