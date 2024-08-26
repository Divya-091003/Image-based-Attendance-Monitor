import os
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
from datetime import datetime
import face_recognition  # Ensure you have face_recognition library installed
import util

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=300)
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray', self.register_new_user, fg="black")
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.attendance_file = './attendance.txt'
        self.start_webcam()

    def start_webcam(self):
        self.cap = cv2.VideoCapture(0)
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        if ret:
            img_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_)
            self.most_recent_capture_arr = frame
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            self.webcam_label.imgtk = imgtk
            self.webcam_label.configure(image=imgtk)
        self.webcam_label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = os.path.join(self.db_dir, 'unknown.png')
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        # Load the unknown image and get its face encodings
        unknown_image = face_recognition.load_image_file(unknown_img_path)
        unknown_face_encodings = face_recognition.face_encodings(unknown_image)

        if len(unknown_face_encodings) == 0:
            util.msg_box('Oops', 'No face found in the image.')
            os.remove(unknown_img_path)
            return

        unknown_face_encoding = unknown_face_encodings[0]

        # Iterate over the database and compare faces
        matches = []
        for file in os.listdir(self.db_dir):
            if file.endswith('.png') and file != 'unknown.png':
                known_image = face_recognition.load_image_file(os.path.join(self.db_dir, file))
                known_face_encodings = face_recognition.face_encodings(known_image)
                if len(known_face_encodings) > 0:
                    known_face_encoding = known_face_encodings[0]
                    match = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)
                    matches.append((file, match[0]))

        name = None
        for file, match in matches:
            if match:
                name = file.split('_')[0]  # Extract the name part
                break

        if name is None:
            util.msg_box('Oops', 'Unknown person! Please register and try again.')
        else:
            util.msg_box('Welcome back!', f'Welcome, {name}!')
            self.mark_attendance(name)

        os.remove(unknown_img_path)

    def mark_attendance(self, name):
        with open(self.attendance_file, 'a') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f'{name} {timestamp}\n')

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+350+100")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = tk.Entry(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = tk.Label(self.register_new_user_window, text='Please, input username:')
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_pil.copy()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get()
        if not name:
            util.msg_box('Error', 'Please enter a valid username.')
            return
        # Get current date and time with underscores instead of spaces
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Convert PIL Image to numpy array
        register_new_user_capture_np = np.array(self.register_new_user_capture)
        # Convert RGB to BGR format as OpenCV expects BGR
        register_new_user_capture_bgr = cv2.cvtColor(register_new_user_capture_np, cv2.COLOR_RGB2BGR)
        # Save the image with timestamp
        cv2.imwrite(os.path.join(self.db_dir, f'{name}_{timestamp}.png'), register_new_user_capture_bgr)
        util.msg_box('Success!', 'User was registered successfully!')
        self.register_new_user_window.destroy()

    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()