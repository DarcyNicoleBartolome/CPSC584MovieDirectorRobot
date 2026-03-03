# import customtkinter as ctk

# ctk.set_appearance_mode("light")
# ctk.set_default_color_theme("blue")


# class MovieDirectorGUI(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("Movie Director Miniature")
#         self.geometry("1000x650")
#         self.minsize(850, 560)

#         # Layout
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_rowconfigure(1, weight=0)
#         self.grid_columnconfigure(0, weight=0)
#         self.grid_columnconfigure(1, weight=1)
#         self.grid_columnconfigure(2, weight=0)

#         # Left side
#         self.left = ctk.CTkFrame(self, corner_radius=16)
#         self.left.grid(row=0, column=0, padx=(18, 10), pady=(18, 10), sticky="ns")

#         for i in range(3):
#             btn = ctk.CTkButton(
#                 self.left,
#                 text="",             
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#                 command=lambda idx=i: self.on_left_action(idx),
#             )
#             btn.grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))

#         # Right side
#         self.right = ctk.CTkFrame(self, corner_radius=16)
#         self.right.grid(row=0, column=2, padx=(10, 18), pady=(18, 10), sticky="ns")

#         for i in range(3):
#             btn = ctk.CTkButton(
#                 self.right,
#                 text="",              
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#                 command=lambda idx=i: self.on_right_action(idx),
#             )
#             btn.grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))

#         # Center for camera
#         self.center = ctk.CTkFrame(self, corner_radius=18)
#         self.center.grid(row=0, column=1, padx=10, pady=(18, 10), sticky="nsew")
#         self.center.grid_rowconfigure(0, weight=1)
#         self.center.grid_columnconfigure(0, weight=1)

#         self.preview = ctk.CTkFrame(self.center, corner_radius=18)
#         self.preview.grid(row=0, column=0, padx=14, pady=14, sticky="nsew")

#         # Crosshair
#         self.crosshair = ctk.CTkLabel(
#             self.preview,
#             text="+",
#             font=ctk.CTkFont(size=44, weight="bold"),
#         )
#         self.crosshair.place(relx=0.5, rely=0.5, anchor="center")

#         # bottom bar
#         self.bottom = ctk.CTkFrame(self, corner_radius=16)
#         self.bottom.grid(row=1, column=0, columnspan=3, padx=18, pady=(10, 18), sticky="ew")
#         self.bottom.grid_columnconfigure(1, weight=1)

#         # D-Pad
#         self.dpad = ctk.CTkFrame(self.bottom, corner_radius=16)
#         self.dpad.grid(row=0, column=0, padx=12, pady=12)

#         for r in range(3):
#             self.dpad.grid_rowconfigure(r, weight=1)
#         for c in range(3):
#             self.dpad.grid_columnconfigure(c, weight=1)

#         def dpad_btn(text, action, r, c):
#             b = ctk.CTkButton(
#                 self.dpad,
#                 text=text,
#                 width=44,
#                 height=44,
#                 corner_radius=14,
#                 command=lambda a=action: self.on_move(a),
#             )
#             b.grid(row=r, column=c, padx=6, pady=6)

#         dpad_btn("▲", "up", 0, 1)
#         dpad_btn("◀", "left", 1, 0)
#         dpad_btn("●", "stop", 1, 1)
#         dpad_btn("▶", "right", 1, 2)
#         dpad_btn("▼", "down", 2, 1)

#     # ---- Callbacks ----
#     def on_left_action(self, idx):
#         print("Left button", idx)

#     def on_right_action(self, idx):
#         print("Right button", idx)

#     def on_move(self, direction):
#         print("Move:", direction)


# if __name__ == "__main__":
#     app = MovieDirectorGUI()
#     app.mainloop()

## streaming using CV stalls 
# import customtkinter as ctk
# import cv2
# from PIL import Image, ImageTk

# ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("blue")


# class MovieDirectorGUI(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("Movie Director Miniature")
#         self.geometry("1000x650")
#         self.minsize(850, 560)

#         self.stream_url = "http://172.17.10.218:8080/"

#         # Layout
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_rowconfigure(1, weight=0)
#         self.grid_columnconfigure(0, weight=0)
#         self.grid_columnconfigure(1, weight=1)
#         self.grid_columnconfigure(2, weight=0)

#         # Left
#         self.left = ctk.CTkFrame(self, corner_radius=16)
#         self.left.grid(row=0, column=0, padx=(18, 10), pady=(18, 10), sticky="ns")
#         for i in range(3):
#             ctk.CTkButton(
#                 self.left, text="", width=52, height=52, corner_radius=14,
#                 command=lambda idx=i: self.on_left_action(idx),
#             ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))

#         # Right
#         self.right = ctk.CTkFrame(self, corner_radius=16)
#         self.right.grid(row=0, column=2, padx=(10, 18), pady=(18, 10), sticky="ns")
#         for i in range(3):
#             ctk.CTkButton(
#                 self.right, text="", width=52, height=52, corner_radius=14,
#                 command=lambda idx=i: self.on_right_action(idx),
#             ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))

#         # Center preview
#         self.center = ctk.CTkFrame(self, corner_radius=18)
#         self.center.grid(row=0, column=1, padx=10, pady=(18, 10), sticky="nsew")
#         self.center.grid_rowconfigure(0, weight=1)
#         self.center.grid_columnconfigure(0, weight=1)

#         self.preview = ctk.CTkFrame(self.center, corner_radius=18)
#         self.preview.grid(row=0, column=0, padx=14, pady=14, sticky="nsew")
#         self.preview.grid_rowconfigure(0, weight=1)
#         self.preview.grid_columnconfigure(0, weight=1)

#         # Label that will hold the frames
#         self.video_label = ctk.CTkLabel(self.preview, text="")
#         self.video_label.grid(row=0, column=0, sticky="nsew")

#         # Crosshair overlay (optional)
#         self.crosshair = ctk.CTkLabel(
#             self.preview, text="+", font=ctk.CTkFont(size=44, weight="bold")
#         )
#         self.crosshair.place(relx=0.5, rely=0.5, anchor="center")

#         # Bottom bar
#         self.bottom = ctk.CTkFrame(self, corner_radius=16)
#         self.bottom.grid(row=1, column=0, columnspan=3, padx=18, pady=(10, 18), sticky="ew")
#         self.bottom.grid_columnconfigure(1, weight=1)

#         self.dpad = ctk.CTkFrame(self.bottom, corner_radius=16)
#         self.dpad.grid(row=0, column=0, padx=12, pady=12)

#         for r in range(3):
#             self.dpad.grid_rowconfigure(r, weight=1)
#         for c in range(3):
#             self.dpad.grid_columnconfigure(c, weight=1)

#         def dpad_btn(text, action, r, c):
#             ctk.CTkButton(
#                 self.dpad,
#                 text=text,
#                 width=44,
#                 height=44,
#                 corner_radius=14,
#                 command=lambda a=action: self.on_move(a),
#             ).grid(row=r, column=c, padx=6, pady=6, sticky="nsew")

#         dpad_btn("▲", "up", 0, 1)
#         dpad_btn("◀", "left", 1, 0)
#         dpad_btn("●", "stop", 1, 1)
#         dpad_btn("▶", "right", 1, 2)
#         dpad_btn("▼", "down", 2, 1)

#         # ---- Stream setup ----
#         self.cap = cv2.VideoCapture(self.stream_url)
#         if not self.cap.isOpened():
#             print("Could not open stream:", self.stream_url)
#             print("Check: can you open http://PI_IP:8080/ in your browser?")
#         else:
#             print("Stream opened:", self.stream_url)

#         self.protocol("WM_DELETE_WINDOW", self.on_close)
#         self.update_video()

#     def update_video(self):
#         if self.cap is None:
#             return

#         ret, frame = self.cap.read()
#         if ret:
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#             # Fit to preview size
#             w = self.preview.winfo_width()
#             h = self.preview.winfo_height()
#             if w > 10 and h > 10:
#                 frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)

#             img = Image.fromarray(frame)
#             imgtk = ImageTk.PhotoImage(img)

#             self.video_label.imgtk = imgtk
#             self.video_label.configure(image=imgtk)

#         # schedule next frame
#         self.after(33, self.update_video)

#     def on_close(self):
#         if self.cap is not None:
#             self.cap.release()
#         self.destroy()

#     # callbacks
#     def on_left_action(self, idx):
#         print("Left button", idx)

#     def on_right_action(self, idx):
#         print("Right button", idx)

#     def on_move(self, direction):
#         print("Move:", direction)


# if __name__ == "__main__":
#     app = MovieDirectorGUI()
#     app.mainloop()



# streaming using CV stalls 
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MovieDirectorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Movie Director Miniature")
        self.geometry("1000x650")
        self.minsize(850, 560)

        self.stream_url = "http://172.17.10.218:8080/"

        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Left
        self.left = ctk.CTkFrame(self, corner_radius=16)
        self.left.grid(row=0, column=0, padx=(18, 10), pady=(18, 10), sticky="ns")
        for i in range(3):
            ctk.CTkButton(
                self.left, text="", width=52, height=52, corner_radius=14,
                command=lambda idx=i: self.on_left_action(idx),
            ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))

        # Right
        self.right = ctk.CTkFrame(self, corner_radius=16)
        self.right.grid(row=0, column=2, padx=(10, 18), pady=(18, 10), sticky="ns")
        for i in range(3):
            ctk.CTkButton(
                self.right, text="", width=52, height=52, corner_radius=14,
                command=lambda idx=i: self.on_right_action(idx),
            ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))

        # Center preview
        self.center = ctk.CTkFrame(self, corner_radius=18)
        self.center.grid(row=0, column=1, padx=10, pady=(18, 10), sticky="nsew")
        self.center.grid_rowconfigure(0, weight=1)
        self.center.grid_columnconfigure(0, weight=1)

        self.preview = ctk.CTkFrame(self.center, corner_radius=18)
        self.preview.grid(row=0, column=0, padx=14, pady=14, sticky="nsew")
        self.preview.grid_rowconfigure(0, weight=1)
        self.preview.grid_columnconfigure(0, weight=1)

        # Label that will hold the frames
        self.video_label = ctk.CTkLabel(self.preview, text="")
        self.video_label.grid(row=0, column=0, sticky="nsew")


        # Bottom bar
        self.bottom = ctk.CTkFrame(self, corner_radius=16)
        self.bottom.grid(row=1, column=0, columnspan=3, padx=18, pady=(10, 18), sticky="ew")
        self.bottom.grid_columnconfigure(1, weight=1)

        self.dpad = ctk.CTkFrame(self.bottom, corner_radius=16)
        self.dpad.grid(row=0, column=0, padx=12, pady=12)

        for r in range(3):
            self.dpad.grid_rowconfigure(r, weight=1)
        for c in range(3):
            self.dpad.grid_columnconfigure(c, weight=1)

        def dpad_btn(text, action, r, c):
            ctk.CTkButton(
                self.dpad,
                text=text,
                width=44,
                height=44,
                corner_radius=14,
                command=lambda a=action: self.on_move(a),
            ).grid(row=r, column=c, padx=6, pady=6, sticky="nsew")

        dpad_btn("▲", "up", 0, 1)
        dpad_btn("◀", "left", 1, 0)
        dpad_btn("●", "stop", 1, 1)
        dpad_btn("▶", "right", 1, 2)
        dpad_btn("▼", "down", 2, 1)

        # ---- Stream setup ----
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Could not open stream:", self.stream_url)
            print("Check: can you open http://PI_IP:8080/ in your browser?")
        else:
            print("Stream opened:", self.stream_url)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update_video()

    def update_video(self):
        if self.cap is None:
            return

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Fit to preview size
            w = self.preview.winfo_width()
            h = self.preview.winfo_height()
            if w > 10 and h > 10:
                frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(img)

            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        # schedule next frame
        self.after(33, self.update_video)

    def on_close(self):
        if self.cap is not None:
            self.cap.release()
        self.destroy()

    # callbacks
    def on_left_action(self, idx):
        print("Left button", idx)

    def on_right_action(self, idx):
        print("Right button", idx)

    def on_move(self, direction):
        print("Move:", direction)


if __name__ == "__main__":
    app = MovieDirectorGUI()
    app.mainloop()

