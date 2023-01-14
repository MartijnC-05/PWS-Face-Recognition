# video https://youtu.be/z_dbnYHAQYg?t=2098

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import util

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")                                                                                                       # window maken
        
        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)                                                     # login knop maken
        self.login_button_main_window.place(x=750, y=200)
        
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray', self.register_new_user, fg='black')      # nieuw gezicht knop maken
        self.register_new_user_button_main_window.place(x=750, y=400)
        
        self.webcam_label = util.get_img_label(self.main_window)                                                                                            # locatie voor webcam
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        
        self.add_webcam(self.webcam_label)
    
    def add_webcam(self, label):                                                                                                                            # webcam openen
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()
        
    def process_webcam(self):                                                                                                                               # zet de webcam in de locatie voor de webcam
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        
        self._label.after(20, self.process_webcam)                                                                                                        # elke 20 miliseconden wordt een nieuwe afbeelding toegevoegd waardoor het een video beeld wordt
        
    def login(self):
        pass
    
    def register_new_user(sefl):
        pass
    
    def start(self):
        self.main_window.mainloop()                                                                                                                         # window starten

if __name__ == "__main__":
    app = App()
    app.start()