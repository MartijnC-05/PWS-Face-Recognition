# video https://youtu.be/z_dbnYHAQYg?t=2098

import os.path
import datetime
import subprocess
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import util

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")                                                                                                           # Window maken
        
        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)                                                         # Login knop maken
        self.login_button_main_window.place(x=750, y=300)
        
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray', self.register_new_user, fg='black')          # Nieuw gezicht knop maken
        self.register_new_user_button_main_window.place(x=750, y=400)
        
        self.webcam_label = util.get_img_label(self.main_window)                                                                                                # Locatie voor webcam
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        
        self.add_webcam(self.webcam_label)                                                                                                                      # Voeg de webcam toe aan de locatie voor de webcam
        
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):                                                                                                                     # Kijken of de opslaglocatie voor de afbeeldingen van gezichten al bestaat
            os.mkdir(self.db_dir)
            
        self.log_path = './log.txt'
    
    def add_webcam(self, label):                                                                                                                                # Webcam openen
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()
        
    def process_webcam(self):                                                                                                                                   # Zet de webcam in de locatie voor de webcam
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        
        self._label.after(20, self.process_webcam)                                                                                                              # Elke 20 miliseconden wordt een nieuwe afbeelding toegevoegd waardoor het een video beeld wordt
        
    def login(self):
        unknown_img_path = './.tmp.jpg'
        
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        
        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))                                                              # Kijken of de meest recente foto wordt herkend
        name = output.split(',')[1][:-3]
        
        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Oh no...', 'Unknown user. Please register new user or try again.')                                                                    # Als de persoon niet herkend is krijgt hij een bericht
            
        else:
            util.msg_box('Welcome!', 'Welcome, {}.'.format(name))                                                                                               # Welkom bericht
            with open(self.log_path, 'a') as f:                                                                                                                 # Houd een log bestand bij die bijhoudt wie en wanneer iemand is ingelogt
                f.write('{},{}\n'.format(name, datetime.datetime.now()))
                f.close
        
        os.remove(unknown_img_path)
    
    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")                                                                                              # Een nieuwe pagina wordt gemaakt voor het opslaan van een nieuw gezicht
        
        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)          # Accepteer knop maken
        self.accept_button_register_new_user_window.place(x=750, y=300)
    
        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)   # Try again knop maken
        self.try_again_button_register_new_user_window.place(x=750, y=400)
    
        self.capture_label = util.get_img_label(self.register_new_user_window)                                                                                  # Foto die wordt gebruikt voor gezichtsherkenning wordt laten zien om te accepteren of opnieuw te proberen
        self.capture_label.place(x=10, y=0, width=700, height=500)
    
        self.add_img_to_label(self.capture_label)
        
        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)                                                                  # Tekst bij tekstvak om te vertellen dat de gebruiker zijn naam daar moet invullen
        self.entry_text_register_new_user.place(x=750, y=150)
        
        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, \ninput username:')                                     # Tekstvak voor de naam van de gebruiker
        self.text_label_register_new_user.place(x=750, y=70)
        
    def try_again_register_new_user(self):                                                                                                                      # Wanneer op try again wordt geklikt ga je terug naar het hoofdmenu
        self.register_new_user_window.destroy()
    
    def add_img_to_label(self, label):                                                                                                                          # De foto die wordt genomen voor de gezichtsherkenning wordt in het frame geplaatst
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        
        self.register_new_user_capture = self.most_recent_capture_arr.copy()
    
    def start(self):
        self.main_window.mainloop()                                                                                                                             # Window starten

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)                                                           # Afbeelding wordt opgeslagen

        util.msg_box('Succes!','User was registered succesfully!')                                                                                              # Melding dat alles goed is gegaan
        
        self.register_new_user_window.destroy()                                                                                                                 # Pagina om nieuwe gebruiker te registreren wordt gesloten

if __name__ == "__main__":
    app = App()
    app.start()                                                                                                                                                 # App starten
