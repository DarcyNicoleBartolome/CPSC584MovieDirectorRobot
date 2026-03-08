# import customtkinter as ctk
# import cv2
# from PIL import Image, ImageTk
# import threading
# import time
# import os

# ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("blue")


# class MovieDirectorGUI(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("Movie Director Miniature")
#         self.geometry("1000x650")
#         self.minsize(850, 560)

#         self.stream_url = "http://172.20.10.2:8080/stream.mjpg"
#         project_dir = os.path.dirname(os.path.abspath(__file__))

#         # Layout
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_rowconfigure(1, weight=0)
#         self.grid_columnconfigure(0, weight=0)
#         self.grid_columnconfigure(1, weight=1)
#         self.grid_columnconfigure(2, weight=0)

#         # Left
#         self.left = ctk.CTkFrame(self, corner_radius=16)
#         self.left.grid(row=0, column=0, padx=(18, 10), pady=(18, 10), sticky="ns")
        
#         # Left side icons: camera, focus, zoom
#         left_icons = ["icons/camera.png", "icons/focus.png", "icons/zoom.png", "icons/joystick.png"]
#         left_photos = []
        
#         for i, icon in enumerate(left_icons):
#             try:
#                 icon_path = os.path.join(project_dir, icon)
#                 icon_img = Image.open(icon_path)
#                 icon_img = icon_img.resize((40, 40), Image.Resampling.LANCZOS)
#                 icon_photo = ImageTk.PhotoImage(icon_img)
#                 left_photos.append(icon_photo)
                
#                 ctk.CTkButton(
#                     self.left, 
#                     image=icon_photo,
#                     text="",
#                     width=52, 
#                     height=52, 
#                     corner_radius=14,
#                     command=lambda idx=i: self.on_left_action(idx),
#                 ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))
#             except Exception as e:
#                 print(f"Error loading {icon}: {e}")
#                 ctk.CTkButton(
#                     self.left, 
#                     text="",
#                     width=52, 
#                     height=52, 
#                     corner_radius=14,
#                     command=lambda idx=i: self.on_left_action(idx),
#                 ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))
        
#         self.left_photos = left_photos  # Keep references

#         # Right
#         self.right = ctk.CTkFrame(self, corner_radius=16)
#         self.right.grid(row=0, column=2, padx=(10, 18), pady=(18, 10), sticky="ns")
        
#         # Right side icons: goldenratio, and others to be added
#         right_icons = ["icons/goldenratio.png", "icons/icon2.png", "icons/icon3.png"]
#         right_photos = []
        
#         for i, icon in enumerate(right_icons):
#             try:
#                 icon_path = os.path.join(project_dir, icon)
#                 icon_img = Image.open(icon_path)
#                 icon_img = icon_img.resize((40, 40), Image.Resampling.LANCZOS)
#                 icon_photo = ImageTk.PhotoImage(icon_img)
#                 right_photos.append(icon_photo)
                
#                 ctk.CTkButton(
#                     self.right, 
#                     image=icon_photo,
#                     text="",
#                     width=52, 
#                     height=52, 
#                     corner_radius=14,
#                     command=lambda idx=i: self.on_right_action(idx),
#                 ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))
#             except Exception as e:
#                 print(f"Error loading {icon}: {e}")
#                 ctk.CTkButton(
#                     self.right, 
#                     text="",
#                     width=52, 
#                     height=52, 
#                     corner_radius=14,
#                     command=lambda idx=i: self.on_right_action(idx),
#                 ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))
        
#         self.right_photos = right_photos  # Keep references

#         # Center preview
#         self.center = ctk.CTkFrame(self, corner_radius=18)
#         self.center.grid(row=0, column=1, padx=10, pady=(18, 10), sticky="nsew")
#         self.center.grid_rowconfigure(0, weight=1)
#         self.center.grid_columnconfigure(0, weight=1)

#         self.preview = ctk.CTkFrame(self.center, corner_radius=18)
#         self.preview.grid(row=0, column=0, padx=14, pady=14, sticky="nsew")
#         self.preview.grid_rowconfigure(0, weight=1)
#         self.preview.grid_columnconfigure(0, weight=1)

#         self.video_label = ctk.CTkLabel(self.preview, text="")
#         self.video_label.grid(row=0, column=0, sticky="nsew")

#         # Bottom bar
#         self.bottom = ctk.CTkFrame(self, corner_radius=16)
#         self.bottom.grid(row=1, column=0, columnspan=3, padx=18, pady=(10, 18), sticky="ew")

#         # ---- Navigation (D-pad) ----
#         self.dpad = ctk.CTkFrame(self.bottom, corner_radius=16)
#         self.dpad.grid(row=0, column=0, padx=12, pady=12, sticky="w")

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

#         # ---- Record Controls (middle) ----
#         self.controls = ctk.CTkFrame(self.bottom, corner_radius=16)
#         self.controls.grid(row=0, column=1, padx=12, pady=12, sticky="ew")

#         # Record button (red) with image
#         try:
#             record_path = os.path.join(project_dir, "icons/record.png")
#             record_img = Image.open(record_path)
#             record_img = record_img.resize((40, 40), Image.Resampling.LANCZOS)
#             record_photo = ImageTk.PhotoImage(record_img)
#             self.record_photo = record_photo  # Keep a reference
            
#             ctk.CTkButton(
#                 self.controls,
#                 image=record_photo,
#                 text="",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#                 fg_color="#CC0000",
#             ).pack(side="left", padx=6)
#         except Exception as e:
#             print(f"Error loading record image: {e}")
#             ctk.CTkButton(
#                 self.controls,
#                 text="●",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#                 fg_color="#CC0000",
#                 text_color="white",
#             ).pack(side="left", padx=6)

#         # Pause button with image
#         try:
#             pause_path = os.path.join(project_dir, "icons/pause.png")
#             pause_img = Image.open(pause_path)
#             pause_img = pause_img.resize((40, 40), Image.Resampling.LANCZOS)
#             pause_photo = ImageTk.PhotoImage(pause_img)
#             self.pause_photo = pause_photo  # Keep a reference
            
#             ctk.CTkButton(
#                 self.controls,
#                 image=pause_photo,
#                 text="",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#             ).pack(side="left", padx=6)
#         except Exception as e:
#             print(f"Error loading pause image: {e}")
#             ctk.CTkButton(
#                 self.controls,
#                 text="⏸",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#             ).pack(side="left", padx=6)

#         # Stop button with image
#         try:
#             stop_path = os.path.join(project_dir, "icons/stop.png")
#             stop_img = Image.open(stop_path)
#             stop_img = stop_img.resize((40, 40), Image.Resampling.LANCZOS)
#             stop_photo = ImageTk.PhotoImage(stop_img)
#             self.stop_photo = stop_photo  # Keep a reference
            
#             ctk.CTkButton(
#                 self.controls,
#                 image=stop_photo,
#                 text="",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#             ).pack(side="left", padx=6)
#         except Exception as e:
#             print(f"Error loading stop image: {e}")
#             ctk.CTkButton(
#                 self.controls,
#                 text="■",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#             ).pack(side="left", padx=6)

#         # ---- Gallery, Speaker, Settings (right) ----
#         self.utility = ctk.CTkFrame(self.bottom, corner_radius=16)
#         self.utility.grid(row=0, column=2, padx=12, pady=12, sticky="e")

#         # Gallery button with image
#         try:
#             gallery_path = os.path.join(project_dir, "icons/gallery.png")
#             gallery_img = Image.open(gallery_path)
#             gallery_img = gallery_img.resize((40, 40), Image.Resampling.LANCZOS)
#             gallery_photo = ImageTk.PhotoImage(gallery_img)
#             self.gallery_photo = gallery_photo  # Keep a reference
            
#             ctk.CTkButton(
#                 self.utility,
#                 image=gallery_photo,
#                 text="",
#                 width=45,
#                 height=45,
#                 corner_radius=14,
#             ).pack(side="left", padx=6)
#         except Exception as e:
#             print(f"Error loading gallery image: {e}")
#             ctk.CTkButton(
#                 self.utility,
#                 text="🖼",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#             ).pack(side="left", padx=6)

#         # Speaker button with image
#         try:
#             speaker_path = os.path.join(project_dir, "icons/speaker.png")
#             speaker_img = Image.open(speaker_path)
#             speaker_img = speaker_img.resize((40, 40), Image.Resampling.LANCZOS)
#             speaker_photo = ImageTk.PhotoImage(speaker_img)
#             self.speaker_photo = speaker_photo  # Keep a reference
            
#             ctk.CTkButton(
#                 self.utility,
#                 image=speaker_photo,
#                 text="",
#                 width=45,
#                 height=45,
#                 corner_radius=14,
#             ).pack(side="left", padx=6)
#         except Exception as e:
#             print(f"Error loading speaker image: {e}")
#             ctk.CTkButton(
#                 self.utility,
#                 text="🔊",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#             ).pack(side="left", padx=6)

#         # Settings button with image
#         try:
#             settings_path = os.path.join(project_dir, "icons/settings.png")
#             settings_img = Image.open(settings_path)
#             settings_img = settings_img.resize((40, 40), Image.Resampling.LANCZOS)
#             settings_photo = ImageTk.PhotoImage(settings_img)
#             self.settings_photo = settings_photo  # Keep a reference
            
#             ctk.CTkButton(
#                 self.utility,
#                 image=settings_photo,
#                 text="",
#                 width=45,
#                 height=45,
#                 corner_radius=14,
#             ).pack(side="left", padx=6)
#         except Exception as e:
#             print(f"Error loading settings image: {e}")
#             ctk.CTkButton(
#                 self.utility,
#                 text="⚙",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#             ).pack(side="left", padx=6)

#         # ---- OpenCV stream state ----
#         self._stop = threading.Event()
#         self._latest_frame_rgb = None
#         self._latest_imgtk = None

#         self.cap = cv2.VideoCapture(self.stream_url, cv2.CAP_FFMPEG)
#         self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

#         if not self.cap.isOpened():
#             print("Could not open stream:", self.stream_url)
#         else:
#             print("Stream opened:", self.stream_url)
#             threading.Thread(target=self._reader_loop, daemon=True).start()

#         self.protocol("WM_DELETE_WINDOW", self.on_close)
#         self.after(33, self._render_latest_frame)

#     def _reader_loop(self):
#         """Read frames in background so GUI never blocks."""
#         while not self._stop.is_set():
#             if self.cap is None:
#                 break

#             ok, frame = self.cap.read()
#             if not ok:
#                 # brief backoff; avoids tight loop when stream drops
#                 time.sleep(0.05)
#                 continue

#             # BGR -> RGB
#             self._latest_frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     def _render_latest_frame(self):
#         frame = self._latest_frame_rgb
#         if frame is not None:
#             w = self.preview.winfo_width()
#             h = self.preview.winfo_height()
#             if w > 10 and h > 10:
#                 frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)

#             img = Image.fromarray(frame)
#             imgtk = ImageTk.PhotoImage(img)
#             self._latest_imgtk = imgtk
#             self.video_label.configure(image=imgtk)

#         self.after(33, self._render_latest_frame)

#     def on_close(self):
#         self._stop.set()
#         try:
#             if self.cap is not None:
#                 self.cap.release()
#         finally:
#             self.destroy()

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









# import customtkinter as ctk
# import cv2
# from PIL import Image, ImageTk
# import threading
# import time
# import os
# from datetime import datetime

# ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("blue")


# class MovieDirectorGUI(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("Movie Director Miniature")
#         self.geometry("1000x650")
#         self.minsize(850, 560)

#         self.stream_url = "http://172.20.10.2:8080/stream.mjpg"
#         project_dir = os.path.dirname(os.path.abspath(__file__))
#         self.recordings_dir = os.path.join(project_dir, "recordings")
#         os.makedirs(self.recordings_dir, exist_ok=True)

#         # ---- Recording state ----
#         self.is_recording = False
#         self.record_start_time = None
#         self.video_writer = None
#         self.recording_filename = None
#         self.record_fps = 20.0
#         self.record_size = None

#         # ---- Layout ----
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_rowconfigure(1, weight=0)
#         self.grid_columnconfigure(0, weight=0)
#         self.grid_columnconfigure(1, weight=1)
#         self.grid_columnconfigure(2, weight=0)

#         # Left
#         self.left = ctk.CTkFrame(self, corner_radius=16)
#         self.left.grid(row=0, column=0, padx=(18, 10), pady=(18, 10), sticky="ns")

#         left_icons = ["icons/camera.png", "icons/focus.png", "icons/zoom.png", "icons/joystick.png"]
#         left_photos = []

#         for i, icon in enumerate(left_icons):
#             try:
#                 icon_path = os.path.join(project_dir, icon)
#                 icon_img = Image.open(icon_path)
#                 icon_img = icon_img.resize((40, 40), Image.Resampling.LANCZOS)
#                 icon_photo = ImageTk.PhotoImage(icon_img)
#                 left_photos.append(icon_photo)

#                 ctk.CTkButton(
#                     self.left,
#                     image=icon_photo,
#                     text="",
#                     width=52,
#                     height=52,
#                     corner_radius=14,
#                     command=lambda idx=i: self.on_left_action(idx),
#                 ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))
#             except Exception as e:
#                 print(f"Error loading {icon}: {e}")
#                 ctk.CTkButton(
#                     self.left,
#                     text="",
#                     width=52,
#                     height=52,
#                     corner_radius=14,
#                     command=lambda idx=i: self.on_left_action(idx),
#                 ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))

#         self.left_photos = left_photos

#         # Right
#         self.right = ctk.CTkFrame(self, corner_radius=16)
#         self.right.grid(row=0, column=2, padx=(10, 18), pady=(18, 10), sticky="ns")

#         right_icons = ["icons/goldenratio.png", "icons/icon2.png", "icons/icon3.png"]
#         right_photos = []

#         for i, icon in enumerate(right_icons):
#             try:
#                 icon_path = os.path.join(project_dir, icon)
#                 icon_img = Image.open(icon_path)
#                 icon_img = icon_img.resize((40, 40), Image.Resampling.LANCZOS)
#                 icon_photo = ImageTk.PhotoImage(icon_img)
#                 right_photos.append(icon_photo)

#                 ctk.CTkButton(
#                     self.right,
#                     image=icon_photo,
#                     text="",
#                     width=52,
#                     height=52,
#                     corner_radius=14,
#                     command=lambda idx=i: self.on_right_action(idx),
#                 ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))
#             except Exception as e:
#                 print(f"Error loading {icon}: {e}")
#                 ctk.CTkButton(
#                     self.right,
#                     text="",
#                     width=52,
#                     height=52,
#                     corner_radius=14,
#                     command=lambda idx=i: self.on_right_action(idx),
#                 ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))

#         self.right_photos = right_photos

#         # Center preview
#         self.center = ctk.CTkFrame(self, corner_radius=18)
#         self.center.grid(row=0, column=1, padx=10, pady=(18, 10), sticky="nsew")
#         self.center.grid_rowconfigure(0, weight=1)
#         self.center.grid_columnconfigure(0, weight=1)

#         self.preview = ctk.CTkFrame(self.center, corner_radius=18)
#         self.preview.grid(row=0, column=0, padx=14, pady=14, sticky="nsew")
#         self.preview.grid_rowconfigure(0, weight=1)
#         self.preview.grid_columnconfigure(0, weight=1)

#         self.video_label = ctk.CTkLabel(self.preview, text="")
#         self.video_label.grid(row=0, column=0, sticky="nsew")

#         # ---- Top overlays ----
#         self.timer_label = ctk.CTkLabel(
#             self.preview,
#             text="",
#             fg_color="#8B0000",
#             text_color="white",
#             corner_radius=10,
#             padx=10,
#             pady=5,
#             font=("Arial", 16, "bold"),
#         )
#         self.timer_label.place(relx=0.5, rely=0.03, anchor="n")
#         self.timer_label.place_forget()

#         self.status_label = ctk.CTkLabel(
#             self.preview,
#             text="Ready",
#             fg_color="gray20",
#             text_color="white",
#             corner_radius=10,
#             padx=10,
#             pady=5,
#             font=("Arial", 14),
#         )
#         self.status_label.place(relx=0.5, rely=0.10, anchor="n")

#         # Bottom bar
#         self.bottom = ctk.CTkFrame(self, corner_radius=16)
#         self.bottom.grid(row=1, column=0, columnspan=3, padx=18, pady=(10, 18), sticky="ew")
#         self.bottom.grid_columnconfigure(1, weight=1)

#         # ---- Navigation (D-pad) ----
#         self.dpad = ctk.CTkFrame(self.bottom, corner_radius=16)
#         self.dpad.grid(row=0, column=0, padx=12, pady=12, sticky="w")

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

#         # ---- Record Controls ----
#         self.controls = ctk.CTkFrame(self.bottom, corner_radius=16)
#         self.controls.grid(row=0, column=1, padx=12, pady=12, sticky="ew")

#         # Record button
#         try:
#             record_path = os.path.join(project_dir, "icons/record.png")
#             record_img = Image.open(record_path)
#             record_img = record_img.resize((40, 40), Image.Resampling.LANCZOS)
#             self.record_photo = ImageTk.PhotoImage(record_img)

#             self.record_button = ctk.CTkButton(
#                 self.controls,
#                 image=self.record_photo,
#                 text="",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#                 fg_color="#CC0000",
#                 hover_color="#990000",
#                 command=self.start_recording,
#             )
#             self.record_button.pack(side="left", padx=6)
#         except Exception as e:
#             print(f"Error loading record image: {e}")
#             self.record_button = ctk.CTkButton(
#                 self.controls,
#                 text="●",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#                 fg_color="#CC0000",
#                 hover_color="#990000",
#                 text_color="white",
#                 command=self.start_recording,
#             )
#             self.record_button.pack(side="left", padx=6)

#         # Pause button
#         try:
#             pause_path = os.path.join(project_dir, "icons/pause.png")
#             pause_img = Image.open(pause_path)
#             pause_img = pause_img.resize((40, 40), Image.Resampling.LANCZOS)
#             self.pause_photo = ImageTk.PhotoImage(pause_img)

#             self.pause_button = ctk.CTkButton(
#                 self.controls,
#                 image=self.pause_photo,
#                 text="",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#                 command=self.pause_recording_placeholder,
#             )
#             self.pause_button.pack(side="left", padx=6)
#         except Exception as e:
#             print(f"Error loading pause image: {e}")
#             self.pause_button = ctk.CTkButton(
#                 self.controls,
#                 text="⏸",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#                 command=self.pause_recording_placeholder,
#             )
#             self.pause_button.pack(side="left", padx=6)

#         # Stop button
#         try:
#             stop_path = os.path.join(project_dir, "icons/stop.png")
#             stop_img = Image.open(stop_path)
#             stop_img = stop_img.resize((40, 40), Image.Resampling.LANCZOS)
#             self.stop_photo = ImageTk.PhotoImage(stop_img)

#             self.stop_button = ctk.CTkButton(
#                 self.controls,
#                 image=self.stop_photo,
#                 text="",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#                 command=self.stop_recording,
#             )
#             self.stop_button.pack(side="left", padx=6)
#         except Exception as e:
#             print(f"Error loading stop image: {e}")
#             self.stop_button = ctk.CTkButton(
#                 self.controls,
#                 text="■",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#                 command=self.stop_recording,
#             )
#             self.stop_button.pack(side="left", padx=6)

#         # ---- Gallery / Speaker / Settings ----
#         self.utility = ctk.CTkFrame(self.bottom, corner_radius=16)
#         self.utility.grid(row=0, column=2, padx=12, pady=12, sticky="e")

#         # Gallery button
#         try:
#             gallery_path = os.path.join(project_dir, "icons/gallery.png")
#             gallery_img = Image.open(gallery_path)
#             gallery_img = gallery_img.resize((40, 40), Image.Resampling.LANCZOS)
#             self.gallery_photo = ImageTk.PhotoImage(gallery_img)

#             self.gallery_button = ctk.CTkButton(
#                 self.utility,
#                 image=self.gallery_photo,
#                 text="",
#                 width=45,
#                 height=45,
#                 corner_radius=14,
#                 command=self.open_gallery,
#             )
#             self.gallery_button.pack(side="left", padx=6)
#         except Exception as e:
#             print(f"Error loading gallery image: {e}")
#             self.gallery_button = ctk.CTkButton(
#                 self.utility,
#                 text= "",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#                 command=self.open_gallery,
#             )
#             self.gallery_button.pack(side="left", padx=6)

#         # Speaker button
#         try:
#             speaker_path = os.path.join(project_dir, "icons/speaker.png")
#             speaker_img = Image.open(speaker_path)
#             speaker_img = speaker_img.resize((40, 40), Image.Resampling.LANCZOS)
#             self.speaker_photo = ImageTk.PhotoImage(speaker_img)

#             ctk.CTkButton(
#                 self.utility,
#                 image=self.speaker_photo,
#                 text="",
#                 width=45,
#                 height=45,
#                 corner_radius=14,
#             ).pack(side="left", padx=6)
#         except Exception as e:
#             print(f"Error loading speaker image: {e}")
#             ctk.CTkButton(
#                 self.utility,
#                 text="🔊",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#             ).pack(side="left", padx=6)

#         # Settings button
#         try:
#             settings_path = os.path.join(project_dir, "icons/settings.png")
#             settings_img = Image.open(settings_path)
#             settings_img = settings_img.resize((40, 40), Image.Resampling.LANCZOS)
#             self.settings_photo = ImageTk.PhotoImage(settings_img)

#             ctk.CTkButton(
#                 self.utility,
#                 image=self.settings_photo,
#                 text="",
#                 width=45,
#                 height=45,
#                 corner_radius=14,
#             ).pack(side="left", padx=6)
#         except Exception as e:
#             print(f"Error loading settings image: {e}")
#             ctk.CTkButton(
#                 self.utility,
#                 text="⚙",
#                 width=52,
#                 height=52,
#                 corner_radius=14,
#             ).pack(side="left", padx=6)

#         # ---- OpenCV stream state ----
#         self._stop = threading.Event()
#         self._latest_frame_rgb = None
#         self._latest_frame_bgr = None
#         self._latest_imgtk = None

#         self.cap = cv2.VideoCapture(self.stream_url, cv2.CAP_FFMPEG)
#         self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

#         if not self.cap.isOpened():
#             print("Could not open stream:", self.stream_url)
#             self.set_status("Could not open stream")
#         else:
#             print("Stream opened:", self.stream_url)
#             self.set_status("Stream opened")
#             threading.Thread(target=self._reader_loop, daemon=True).start()

#         self.protocol("WM_DELETE_WINDOW", self.on_close)
#         self.after(33, self._render_latest_frame)
#         self.after(250, self._update_recording_timer)

#     def set_status(self, message):
#         self.status_label.configure(text=message)

#     def _reader_loop(self):
#         while not self._stop.is_set():
#             if self.cap is None:
#                 break

#             ok, frame = self.cap.read()
#             if not ok:
#                 time.sleep(0.05)
#                 continue

#             self._latest_frame_bgr = frame.copy()
#             self._latest_frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#             if self.is_recording and self.video_writer is not None:
#                 try:
#                     self.video_writer.write(frame)
#                 except Exception as e:
#                     print("Recording write error:", e)

#     def _render_latest_frame(self):
#         frame = self._latest_frame_rgb
#         if frame is not None:
#             w = self.preview.winfo_width()
#             h = self.preview.winfo_height()
#             if w > 10 and h > 10:
#                 resized = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
#             else:
#                 resized = frame

#             img = Image.fromarray(resized)
#             imgtk = ImageTk.PhotoImage(img)
#             self._latest_imgtk = imgtk
#             self.video_label.configure(image=imgtk)

#         self.after(33, self._render_latest_frame)

#     def _update_recording_timer(self):
#         if self.is_recording and self.record_start_time is not None:
#             elapsed = int(time.time() - self.record_start_time)
#             mins = elapsed // 60
#             secs = elapsed % 60
#             self.timer_label.configure(text=f"● REC  {mins:02d}:{secs:02d}")
#             self.timer_label.place(relx=0.5, rely=0.03, anchor="n")
#         else:
#             self.timer_label.place_forget()

#         self.after(250, self._update_recording_timer)

#     def start_recording(self):
#         if self.is_recording:
#             self.set_status("Already recording")
#             return

#         if self._latest_frame_bgr is None:
#             self.set_status("No video frame available yet")
#             return

#         frame = self._latest_frame_bgr
#         h, w = frame.shape[:2]
#         self.record_size = (w, h)

#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         self.recording_filename = os.path.join(self.recordings_dir, f"recording_{timestamp}.avi")

#         fourcc = cv2.VideoWriter_fourcc(*"XVID")
#         self.video_writer = cv2.VideoWriter(
#             self.recording_filename,
#             fourcc,
#             self.record_fps,
#             self.record_size
#         )

#         if not self.video_writer.isOpened():
#             self.video_writer = None
#             self.set_status("Failed to start recording")
#             return

#         self.is_recording = True
#         self.record_start_time = time.time()
#         self.set_status("Recording started")
#         print("Recording started:", self.recording_filename)

#     def stop_recording(self):
#         if not self.is_recording:
#             self.set_status("Not currently recording")
#             return

#         self.is_recording = False
#         self.record_start_time = None

#         if self.video_writer is not None:
#             self.video_writer.release()
#             self.video_writer = None

#         saved_name = os.path.basename(self.recording_filename) if self.recording_filename else "video"
#         self.set_status(f"Saved: {saved_name}")
#         print("Saved recording:", self.recording_filename)

#     def pause_recording_placeholder(self):
#         self.set_status("Pause not implemented yet")

#     def get_recordings(self):
#         files = []
#         for f in os.listdir(self.recordings_dir):
#             if f.lower().endswith((".avi", ".mp4", ".mov", ".mkv")):
#                 files.append(f)
#         files.sort(reverse=True)
#         return files

#     def open_gallery(self):
#         files = self.get_recordings()

#         gallery = ctk.CTkToplevel(self)
#         gallery.title("Gallery")
#         gallery.geometry("500x400")

#         ctk.CTkLabel(gallery, text="Saved Recordings", font=("Arial", 20, "bold")).pack(pady=12)

#         scroll = ctk.CTkScrollableFrame(gallery, width=440, height=260)
#         scroll.pack(padx=12, pady=12, fill="both", expand=True)

#         if not files:
#             ctk.CTkLabel(scroll, text="No recordings found").pack(pady=10)
#             return

#         for filename in files:
#             row = ctk.CTkFrame(scroll)
#             row.pack(fill="x", padx=6, pady=6)

#             ctk.CTkLabel(row, text=filename, anchor="w").pack(side="left", padx=8, pady=8)

#             ctk.CTkButton(
#                 row,
#                 text="Play",
#                 width=80,
#                 command=lambda f=filename: self.play_recording(os.path.join(self.recordings_dir, f))
#             ).pack(side="right", padx=8, pady=8)

#     def play_recording(self, filepath):
#         player = ctk.CTkToplevel(self)
#         player.title(os.path.basename(filepath))
#         player.geometry("800x500")

#         video_frame = ctk.CTkLabel(player, text="")
#         video_frame.pack(fill="both", expand=True, padx=10, pady=10)

#         info_label = ctk.CTkLabel(player, text=f"Playing: {os.path.basename(filepath)}")
#         info_label.pack(pady=(0, 10))

#         cap = cv2.VideoCapture(filepath)

#         if not cap.isOpened():
#             info_label.configure(text="Failed to open video")
#             return

#         def update_video():
#             if not player.winfo_exists():
#                 cap.release()
#                 return

#             ok, frame = cap.read()
#             if not ok:
#                 cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#                 ok, frame = cap.read()
#                 if not ok:
#                     cap.release()
#                     return

#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#             w = max(video_frame.winfo_width(), 100)
#             h = max(video_frame.winfo_height(), 100)
#             frame_rgb = cv2.resize(frame_rgb, (w, h), interpolation=cv2.INTER_AREA)

#             img = Image.fromarray(frame_rgb)
#             imgtk = ImageTk.PhotoImage(img)
#             video_frame.imgtk = imgtk
#             video_frame.configure(image=imgtk)

#             player.after(33, update_video)

#         def on_player_close():
#             cap.release()
#             player.destroy()

#         player.protocol("WM_DELETE_WINDOW", on_player_close)
#         update_video()

#     def on_close(self):
#         self._stop.set()

#         if self.is_recording:
#             self.stop_recording()

#         try:
#             if self.cap is not None:
#                 self.cap.release()
#         finally:
#             self.destroy()

#     def on_left_action(self, idx):
#         print("Left button", idx)

#     def on_right_action(self, idx):
#         print("Right button", idx)

#     def on_move(self, direction):
#         print("Move:", direction)


# if __name__ == "__main__":
#     app = MovieDirectorGUI()
#     app.mainloop()



import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import threading
import time
import os
import subprocess
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MovieDirectorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Movie Director Miniature")
        self.geometry("1000x650")
        self.minsize(850, 560)

        self.stream_url = "http://172.20.10.2:8080/stream.mjpg"
        self.pi_host = "172.20.10.2"
        self.pi_user = "group5"

        self.move_commands = {
            "up": "python3 ~/pi/picrawler/examples/remote_move.py forward",
            "down": "python3 ~/pi/picrawler/examples/remote_move.py backward",
            "left": "python3 ~/pi/picrawler/examples/remote_move.py left",
            "right": "python3 ~/pi/picrawler/examples/remote_move.py right",
            "stop": "python3 ~/pi/picrawler/examples/remote_move.py stop",
        }

        self.last_move_time = 0

        self.current_direction = None
        self.command_lock = threading.Lock()

        project_dir = os.path.dirname(os.path.abspath(__file__))
        self.recordings_dir = os.path.join(project_dir, "recordings")
        os.makedirs(self.recordings_dir, exist_ok=True)

        # ---- Recording state ----
        self.is_recording = False
        self.record_start_time = None
        self.video_writer = None
        self.recording_filename = None
        self.record_fps = 20.0
        self.record_size = None

        # ---- Layout ----
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Left
        self.left = ctk.CTkFrame(self, corner_radius=16)
        self.left.grid(row=0, column=0, padx=(18, 10), pady=(18, 10), sticky="ns")

        left_icons = ["icons/camera.png", "icons/focus.png", "icons/zoom.png", "icons/joystick.png"]
        left_photos = []

        for i, icon in enumerate(left_icons):
            try:
                icon_path = os.path.join(project_dir, icon)
                icon_img = Image.open(icon_path)
                icon_img = icon_img.resize((40, 40), Image.Resampling.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon_img)
                left_photos.append(icon_photo)

                ctk.CTkButton(
                    self.left,
                    image=icon_photo,
                    text="",
                    width=52,
                    height=52,
                    corner_radius=14,
                    command=lambda idx=i: self.on_left_action(idx),
                ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))
            except Exception as e:
                print(f"Error loading {icon}: {e}")
                ctk.CTkButton(
                    self.left,
                    text="",
                    width=52,
                    height=52,
                    corner_radius=14,
                    command=lambda idx=i: self.on_left_action(idx),
                ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))

        self.left_photos = left_photos

        # Right
        self.right = ctk.CTkFrame(self, corner_radius=16)
        self.right.grid(row=0, column=2, padx=(10, 18), pady=(18, 10), sticky="ns")

        right_icons = ["icons/goldenratio.png", "icons/icon2.png", "icons/icon3.png"]
        right_photos = []

        for i, icon in enumerate(right_icons):
            try:
                icon_path = os.path.join(project_dir, icon)
                icon_img = Image.open(icon_path)
                icon_img = icon_img.resize((40, 40), Image.Resampling.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon_img)
                right_photos.append(icon_photo)

                ctk.CTkButton(
                    self.right,
                    image=icon_photo,
                    text="",
                    width=52,
                    height=52,
                    corner_radius=14,
                    command=lambda idx=i: self.on_right_action(idx),
                ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))
            except Exception as e:
                print(f"Error loading {icon}: {e}")
                ctk.CTkButton(
                    self.right,
                    text="",
                    width=52,
                    height=52,
                    corner_radius=14,
                    command=lambda idx=i: self.on_right_action(idx),
                ).grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))

        self.right_photos = right_photos

        # Center preview
        self.center = ctk.CTkFrame(self, corner_radius=18)
        self.center.grid(row=0, column=1, padx=10, pady=(18, 10), sticky="nsew")
        self.center.grid_rowconfigure(0, weight=1)
        self.center.grid_columnconfigure(0, weight=1)

        self.preview = ctk.CTkFrame(self.center, corner_radius=18)
        self.preview.grid(row=0, column=0, padx=14, pady=14, sticky="nsew")
        self.preview.grid_rowconfigure(0, weight=1)
        self.preview.grid_columnconfigure(0, weight=1)

        self.video_label = ctk.CTkLabel(self.preview, text="")
        self.video_label.grid(row=0, column=0, sticky="nsew")

        # ---- Top overlays ----
        self.timer_label = ctk.CTkLabel(
            self.preview,
            text="",
            fg_color="#8B0000",
            text_color="white",
            corner_radius=10,
            padx=10,
            pady=5,
            font=("Arial", 16, "bold"),
        )
        self.timer_label.place(relx=0.5, rely=0.03, anchor="n")
        self.timer_label.place_forget()

        self.status_label = ctk.CTkLabel(
            self.preview,
            text="Ready",
            fg_color="gray20",
            text_color="white",
            corner_radius=10,
            padx=10,
            pady=5,
            font=("Arial", 14),
        )
        self.status_label.place(relx=0.5, rely=0.10, anchor="n")

        # Bottom bar
        self.bottom = ctk.CTkFrame(self, corner_radius=16)
        self.bottom.grid(row=1, column=0, columnspan=3, padx=18, pady=(10, 18), sticky="ew")
        self.bottom.grid_columnconfigure(1, weight=1)

        # ---- Navigation (D-pad) ----
        self.dpad = ctk.CTkFrame(self.bottom, corner_radius=16)
        self.dpad.grid(row=0, column=0, padx=12, pady=12, sticky="w")

        for r in range(3):
            self.dpad.grid_rowconfigure(r, weight=1)
        for c in range(3):
            self.dpad.grid_columnconfigure(c, weight=1)


        def dpad_btn(text, action, r, c):
            btn = ctk.CTkButton(
                self.dpad,
                text=text,
                width=44,
                height=44,
                corner_radius=14,
                command=lambda a=action: self.on_move(a),
            )
            btn.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")
            return btn

        self.btn_up = dpad_btn("▲", "up", 0, 1)
        self.btn_left = dpad_btn("◀", "left", 1, 0)
        self.btn_stop = dpad_btn("●", "stop", 1, 1)
        self.btn_right = dpad_btn("▶", "right", 1, 2)
        self.btn_down = dpad_btn("▼", "down", 2, 1)

        
        # ---- Record Controls ----
        self.controls = ctk.CTkFrame(self.bottom, corner_radius=16)
        self.controls.grid(row=0, column=1, padx=12, pady=12, sticky="ew")

        # Record button
        try:
            record_path = os.path.join(project_dir, "icons/record.png")
            record_img = Image.open(record_path)
            record_img = record_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.record_photo = ImageTk.PhotoImage(record_img)

            self.record_button = ctk.CTkButton(
                self.controls,
                image=self.record_photo,
                text="",
                width=52,
                height=52,
                corner_radius=14,
                fg_color="#CC0000",
                hover_color="#990000",
                command=self.start_recording,
            )
            self.record_button.pack(side="left", padx=6)
        except Exception as e:
            print(f"Error loading record image: {e}")
            self.record_button = ctk.CTkButton(
                self.controls,
                text="●",
                width=52,
                height=52,
                corner_radius=14,
                fg_color="#CC0000",
                hover_color="#990000",
                text_color="white",
                command=self.start_recording,
            )
            self.record_button.pack(side="left", padx=6)

        # Pause button
        try:
            pause_path = os.path.join(project_dir, "icons/pause.png")
            pause_img = Image.open(pause_path)
            pause_img = pause_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.pause_photo = ImageTk.PhotoImage(pause_img)

            self.pause_button = ctk.CTkButton(
                self.controls,
                image=self.pause_photo,
                text="",
                width=52,
                height=52,
                corner_radius=14,
                command=self.pause_recording_placeholder,
            )
            self.pause_button.pack(side="left", padx=6)
        except Exception as e:
            print(f"Error loading pause image: {e}")
            self.pause_button = ctk.CTkButton(
                self.controls,
                text="⏸",
                width=52,
                height=52,
                corner_radius=14,
                command=self.pause_recording_placeholder,
            )
            self.pause_button.pack(side="left", padx=6)

        # Stop button
        try:
            stop_path = os.path.join(project_dir, "icons/stop.png")
            stop_img = Image.open(stop_path)
            stop_img = stop_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.stop_photo = ImageTk.PhotoImage(stop_img)

            self.stop_button = ctk.CTkButton(
                self.controls,
                image=self.stop_photo,
                text="",
                width=52,
                height=52,
                corner_radius=14,
                command=self.stop_recording,
            )
            self.stop_button.pack(side="left", padx=6)
        except Exception as e:
            print(f"Error loading stop image: {e}")
            self.stop_button = ctk.CTkButton(
                self.controls,
                text="■",
                width=52,
                height=52,
                corner_radius=14,
                command=self.stop_recording,
            )
            self.stop_button.pack(side="left", padx=6)

        # ---- Gallery / Speaker / Settings ----
        self.utility = ctk.CTkFrame(self.bottom, corner_radius=16)
        self.utility.grid(row=0, column=2, padx=12, pady=12, sticky="e")

        # Gallery button
        try:
            gallery_path = os.path.join(project_dir, "icons/gallery.png")
            gallery_img = Image.open(gallery_path)
            gallery_img = gallery_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.gallery_photo = ImageTk.PhotoImage(gallery_img)

            self.gallery_button = ctk.CTkButton(
                self.utility,
                image=self.gallery_photo,
                text="",
                width=45,
                height=45,
                corner_radius=14,
                command=self.open_gallery,
            )
            self.gallery_button.pack(side="left", padx=6)
        except Exception as e:
            print(f"Error loading gallery image: {e}")
            self.gallery_button = ctk.CTkButton(
                self.utility,
                text="🖼",
                width=52,
                height=52,
                corner_radius=14,
                command=self.open_gallery,
            )
            self.gallery_button.pack(side="left", padx=6)

        # Speaker button
        try:
            speaker_path = os.path.join(project_dir, "icons/speaker.png")
            speaker_img = Image.open(speaker_path)
            speaker_img = speaker_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.speaker_photo = ImageTk.PhotoImage(speaker_img)

            ctk.CTkButton(
                self.utility,
                image=self.speaker_photo,
                text="",
                width=45,
                height=45,
                corner_radius=14,
            ).pack(side="left", padx=6)
        except Exception as e:
            print(f"Error loading speaker image: {e}")
            ctk.CTkButton(
                self.utility,
                text="🔊",
                width=52,
                height=52,
                corner_radius=14,
            ).pack(side="left", padx=6)

        # Settings button
        try:
            settings_path = os.path.join(project_dir, "icons/settings.png")
            settings_img = Image.open(settings_path)
            settings_img = settings_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.settings_photo = ImageTk.PhotoImage(settings_img)

            ctk.CTkButton(
                self.utility,
                image=self.settings_photo,
                text="",
                width=45,
                height=45,
                corner_radius=14,
            ).pack(side="left", padx=6)
        except Exception as e:
            print(f"Error loading settings image: {e}")
            ctk.CTkButton(
                self.utility,
                text="⚙",
                width=52,
                height=52,
                corner_radius=14,
            ).pack(side="left", padx=6)

        # ---- OpenCV stream state ----
        self._stop = threading.Event()
        self._latest_frame_rgb = None
        self._latest_frame_bgr = None
        self._latest_imgtk = None

        self.cap = cv2.VideoCapture(self.stream_url, cv2.CAP_FFMPEG)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            print("Could not open stream:", self.stream_url)
            self.set_status("Could not open stream")
        else:
            print("Stream opened:", self.stream_url)
            self.set_status("Stream opened")
            threading.Thread(target=self._reader_loop, daemon=True).start()

        # Keyboard control
        self.bind("<w>", lambda e: self.on_move("up"))
        self.bind("<s>", lambda e: self.on_move("down"))
        self.bind("<a>", lambda e: self.on_move("left"))
        self.bind("<d>", lambda e: self.on_move("right"))
        self.bind("<space>", lambda e: self.on_move("stop"))

        self.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(33, self._render_latest_frame)
        self.after(250, self._update_recording_timer)

    def set_status(self, message):
        self.status_label.configure(text=message)

    def _reader_loop(self):
        while not self._stop.is_set():
            if self.cap is None:
                break

            ok, frame = self.cap.read()
            if not ok:
                time.sleep(0.05)
                continue

            self._latest_frame_bgr = frame.copy()
            self._latest_frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if self.is_recording and self.video_writer is not None:
                try:
                    self.video_writer.write(frame)
                except Exception as e:
                    print("Recording write error:", e)

    def _render_latest_frame(self):
        frame = self._latest_frame_rgb
        if frame is not None:
            w = self.preview.winfo_width()
            h = self.preview.winfo_height()
            if w > 10 and h > 10:
                resized = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
            else:
                resized = frame

            img = Image.fromarray(resized)
            imgtk = ImageTk.PhotoImage(img)
            self._latest_imgtk = imgtk
            self.video_label.configure(image=imgtk)

        self.after(33, self._render_latest_frame)

    def _update_recording_timer(self):
        if self.is_recording and self.record_start_time is not None:
            elapsed = int(time.time() - self.record_start_time)
            mins = elapsed // 60
            secs = elapsed % 60
            self.timer_label.configure(text=f"● REC  {mins:02d}:{secs:02d}")
            self.timer_label.place(relx=0.5, rely=0.03, anchor="n")
        else:
            self.timer_label.place_forget()

        self.after(250, self._update_recording_timer)

    def start_recording(self):
        if self.is_recording:
            self.set_status("Already recording")
            return

        if self._latest_frame_bgr is None:
            self.set_status("No video frame available yet")
            return

        frame = self._latest_frame_bgr
        h, w = frame.shape[:2]
        self.record_size = (w, h)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.recording_filename = os.path.join(self.recordings_dir, f"recording_{timestamp}.avi")

        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.video_writer = cv2.VideoWriter(
            self.recording_filename,
            fourcc,
            self.record_fps,
            self.record_size
        )

        if not self.video_writer.isOpened():
            self.video_writer = None
            self.set_status("Failed to start recording")
            return

        self.is_recording = True
        self.record_start_time = time.time()
        self.set_status("Recording started")
        print("Recording started:", self.recording_filename)

    def stop_recording(self):
        if not self.is_recording:
            self.set_status("Not currently recording")
            return

        self.is_recording = False
        self.record_start_time = None

        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None

        saved_name = os.path.basename(self.recording_filename) if self.recording_filename else "video"
        self.set_status(f"Saved: {saved_name}")
        print("Saved recording:", self.recording_filename)

    def pause_recording_placeholder(self):
        self.set_status("Pause not implemented yet")

    def get_recordings(self):
        files = []
        for f in os.listdir(self.recordings_dir):
            if f.lower().endswith((".avi", ".mp4", ".mov", ".mkv")):
                files.append(f)
        files.sort(reverse=True)
        return files

    def open_gallery(self):
        files = self.get_recordings()

        gallery = ctk.CTkToplevel(self)
        gallery.title("Gallery")
        gallery.geometry("500x400")

        ctk.CTkLabel(gallery, text="Saved Recordings", font=("Arial", 20, "bold")).pack(pady=12)

        scroll = ctk.CTkScrollableFrame(gallery, width=440, height=260)
        scroll.pack(padx=12, pady=12, fill="both", expand=True)

        if not files:
            ctk.CTkLabel(scroll, text="No recordings found").pack(pady=10)
            return

        for filename in files:
            row = ctk.CTkFrame(scroll)
            row.pack(fill="x", padx=6, pady=6)

            ctk.CTkLabel(row, text=filename, anchor="w").pack(side="left", padx=8, pady=8)

            ctk.CTkButton(
                row,
                text="Play",
                width=80,
                command=lambda f=filename: self.play_recording(os.path.join(self.recordings_dir, f))
            ).pack(side="right", padx=8, pady=8)

    def play_recording(self, filepath):
        player = ctk.CTkToplevel(self)
        player.title(os.path.basename(filepath))
        player.geometry("800x500")

        video_frame = ctk.CTkLabel(player, text="")
        video_frame.pack(fill="both", expand=True, padx=10, pady=10)

        info_label = ctk.CTkLabel(player, text=f"Playing: {os.path.basename(filepath)}")
        info_label.pack(pady=(0, 10))

        cap = cv2.VideoCapture(filepath)

        if not cap.isOpened():
            info_label.configure(text="Failed to open video")
            return

        def update_video():
            if not player.winfo_exists():
                cap.release()
                return

            ok, frame = cap.read()
            if not ok:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ok, frame = cap.read()
                if not ok:
                    cap.release()
                    return

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            w = max(video_frame.winfo_width(), 100)
            h = max(video_frame.winfo_height(), 100)
            frame_rgb = cv2.resize(frame_rgb, (w, h), interpolation=cv2.INTER_AREA)

            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(img)
            video_frame.imgtk = imgtk
            video_frame.configure(image=imgtk)

            player.after(33, update_video)

        def on_player_close():
            cap.release()
            player.destroy()

        player.protocol("WM_DELETE_WINDOW", on_player_close)
        update_video()

    # def run_pi_command(self, command):
    #     def worker():
    #         try:
    #             ssh_cmd = [
    #                 "ssh",
    #                 f"{self.pi_user}@{self.pi_host}",
    #                 command
    #             ]
    #             result = subprocess.run(
    #                 ssh_cmd,
    #                 capture_output=True,
    #                 text=True,
    #                 timeout=5
    #             )

    #             if result.returncode != 0:
    #                 err = result.stderr.strip() or "Unknown SSH error"
    #                 print("Pi command error:", err)
    #                 self.after(0, lambda: self.set_status(f"Move error: {err}"))
    #             else:
    #                 print("Pi command ok:", command)

    #         except subprocess.TimeoutExpired:
    #             print("Pi command timeout:", command)
    #             self.after(0, lambda: self.set_status("Move timeout"))
    #         except Exception as e:
    #             print("Pi command exception:", e)
    #             self.after(0, lambda: self.set_status(f"Move failed: {e}"))

    #     threading.Thread(target=worker, daemon=True).start()

    # def send_move_command(self, direction):
    #     command = self.move_commands.get(direction)
    #     if not command:
    #         self.set_status(f"No command set for {direction}")
    #         return

    #     print("Sending move:", direction, "->", command)
    #     self.set_status(f"Moving {direction}")
    #     self.run_pi_command(command)

    # def on_move_press(self, direction):
    #     with self.command_lock:
    #         if self.current_direction == direction:
    #             return
    #         self.current_direction = direction

    #     self.send_move_command(direction)

    # def on_move_release(self):
        # with self.command_lock:
        #     if self.current_direction is None:
        #         return
        #     self.current_direction = None

        # self.send_move_command("stop")


    def run_pi_command(self, command):
        def worker():
            try:
                ssh_cmd = [
                    "ssh",
                    "-o", "BatchMode=yes",
                    "-o", "ConnectTimeout=3",
                    f"{self.pi_user}@{self.pi_host}",
                    command
                ]

                result = subprocess.run(
                    ssh_cmd,
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if result.returncode != 0:
                    err = result.stderr.strip() or "Unknown SSH error"
                    print("Pi command error:", err)
                    self.after(0, lambda: self.set_status("Move error"))
                else:
                    print("Pi command ok:", command)

            except subprocess.TimeoutExpired:
                print("Pi command timeout:", command)
                self.after(0, lambda: self.set_status("Move timeout"))
            except Exception as e:
                print("Pi command exception:", e)
                self.after(0, lambda: self.set_status("Move failed"))

        threading.Thread(target=worker, daemon=True).start()

    def send_move_command(self, direction):
        now = time.time()
        if now - self.last_move_time < 0.35:
            return

        self.last_move_time = now

        command = self.move_commands.get(direction)
        if not command:
            self.set_status(f"No command set for {direction}")
            return

        print("Sending move:", direction, "->", command)
        self.set_status(f"Moving {direction}")
        self.run_pi_command(command)

    def on_move(self, direction):
        self.send_move_command(direction)
    def on_close(self):
        self._stop.set()

        try:
            self.send_move_command("stop")
        except Exception:
            pass

        if self.is_recording:
            self.stop_recording()

        try:
            if self.cap is not None:
                self.cap.release()
        finally:
            self.destroy()

    # callbacks
    def on_left_action(self, idx):
        print("Left button", idx)

    def on_right_action(self, idx):
        print("Right button", idx)


if __name__ == "__main__":
    app = MovieDirectorGUI()
    app.mainloop()