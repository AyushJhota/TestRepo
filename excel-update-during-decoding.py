import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import threading

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
                access_status = check_access(data, "ticket_data.xlsx")
                print(access_status)  # Print the access status
                if access_status == "Grant Access!":
                    update_excel(data, "ticket_data.xlsx")
                # Add any further processing here
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.waitKey(2000)  # Add a delay of (1000 = 1) seconds before scanning again

        self.capture.release()
        cv2.destroyAllWindows()

def check_access(data, excel_file):
    df = pd.read_excel(excel_file)
    if data in df.values:
        print("Grant Access!")
        return "Grant Access!"
    else:
        print("No Entry!")
        return "No Entry!"

def update_excel(data, excel_file):
    df = pd.read_excel(excel_file)
    idx = df.index[df["Ticket Code"] == data].tolist()[0]
    df.at[idx, "Scanned"] = "Yes"
    df.to_excel(excel_file, index=False)
    print("Excel file updated.")

if __name__ == "__main__":
    scanner = QRCodeScanner()
    scanner.start_scan()
