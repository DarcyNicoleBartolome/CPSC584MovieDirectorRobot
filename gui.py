import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import threading
import time
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MovieDirectorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Movie Director Miniature")
        self.geometry("1000x650")
        self.minsize(850, 560)

        self.stream_url = "http://172.17.10.218:8080/stream.mjpg"

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

        self.video_label = ctk.CTkLabel(self.preview, text="")
        self.video_label.grid(row=0, column=0, sticky="nsew")

        # Bottom bar
        self.bottom = ctk.CTkFrame(self, corner_radius=16)
        self.bottom.grid(row=1, column=0, columnspan=3, padx=18, pady=(10, 18), sticky="ew")

        # ---- Navigation (D-pad) ----
        self.dpad = ctk.CTkFrame(self.bottom, corner_radius=16)
        self.dpad.grid(row=0, column=0, padx=12, pady=12, sticky="w")

        project_dir = os.path.dirname(os.path.abspath(__file__))

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

        # ---- Record Controls (middle) ----
        self.controls = ctk.CTkFrame(self.bottom, corner_radius=16)
        self.controls.grid(row=0, column=1, padx=12, pady=12, sticky="ew")

        # Record button (red) with image
        try:
            record_path = os.path.join(project_dir, "record.png")
            record_img = Image.open(record_path)
            record_img = record_img.resize((40, 40), Image.Resampling.LANCZOS)
            record_photo = ImageTk.PhotoImage(record_img)
            self.record_photo = record_photo  # Keep a reference
            
            ctk.CTkButton(
                self.controls,
                image=record_photo,
                text="",
                width=52,
                height=52,
                corner_radius=14,
                fg_color="#CC0000",
            ).pack(side="left", padx=6)
        except Exception as e:
            print(f"Error loading record image: {e}")
            ctk.CTkButton(
                self.controls,
                text="●",
                width=52,
                height=52,
                corner_radius=14,
                fg_color="#CC0000",
                text_color="white",
            ).pack(side="left", padx=6)

        # Pause button with image
        try:
            pause_path = os.path.join(project_dir, "pause.png")
            pause_img = Image.open(pause_path)
            pause_img = pause_img.resize((40, 40), Image.Resampling.LANCZOS)
            pause_photo = ImageTk.PhotoImage(pause_img)
            self.pause_photo = pause_photo  # Keep a reference
            
            ctk.CTkButton(
                self.controls,
                image=pause_photo,
                text="",
                width=52,
                height=52,
                corner_radius=14,
            ).pack(side="left", padx=6)
        except Exception as e:
            print(f"Error loading pause image: {e}")
            ctk.CTkButton(
                self.controls,
                text="⏸",
                width=52,
                height=52,
                corner_radius=14,
            ).pack(side="left", padx=6)

        # Stop button with image
        try:
            stop_path = os.path.join(project_dir, "stop.png")
            stop_img = Image.open(stop_path)
            stop_img = stop_img.resize((40, 40), Image.Resampling.LANCZOS)
            stop_photo = ImageTk.PhotoImage(stop_img)
            self.stop_photo = stop_photo  # Keep a reference
            
            ctk.CTkButton(
                self.controls,
                image=stop_photo,
                text="",
                width=52,
                height=52,
                corner_radius=14,
            ).pack(side="left", padx=6)
        except Exception as e:
            print(f"Error loading stop image: {e}")
            ctk.CTkButton(
                self.controls,
                text="■",
                width=52,
                height=52,
                corner_radius=14,
            ).pack(side="left", padx=6)

        # ---- Gallery, Speaker, Settings (right) ----
        self.utility = ctk.CTkFrame(self.bottom, corner_radius=16)
        self.utility.grid(row=0, column=2, padx=12, pady=12, sticky="e")

        # Gallery button with image
        try:
            gallery_path = os.path.join(project_dir, "gallery.png")
            gallery_img = Image.open(gallery_path)
            gallery_img = gallery_img.resize((40, 40), Image.Resampling.LANCZOS)
            gallery_photo = ImageTk.PhotoImage(gallery_img)
            self.gallery_photo = gallery_photo  # Keep a reference
            
            ctk.CTkButton(
                self.utility,
                image=gallery_photo,
                text="",
                width=45,
                height=45,
                corner_radius=14,
            ).pack(side="left", padx=6)
        except Exception as e:
            print(f"Error loading gallery image: {e}")
            ctk.CTkButton(
                self.utility,
                text="🖼",
                width=52,
                height=52,
                corner_radius=14,
            ).pack(side="left", padx=6)

        # Speaker button with image
        try:
            speaker_path = os.path.join(project_dir, "speaker.png")
            speaker_img = Image.open(speaker_path)
            speaker_img = speaker_img.resize((40, 40), Image.Resampling.LANCZOS)
            speaker_photo = ImageTk.PhotoImage(speaker_img)
            self.speaker_photo = speaker_photo  # Keep a reference
            
            ctk.CTkButton(
                self.utility,
                image=speaker_photo,
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

        # Settings button with image
        try:
            settings_path = os.path.join(project_dir, "settings.png")
            settings_img = Image.open(settings_path)
            settings_img = settings_img.resize((40, 40), Image.Resampling.LANCZOS)
            settings_photo = ImageTk.PhotoImage(settings_img)
            self.settings_photo = settings_photo  # Keep a reference
            
            ctk.CTkButton(
                self.utility,
                image=settings_photo,
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
        self._latest_imgtk = None

        self.cap = cv2.VideoCapture(self.stream_url, cv2.CAP_FFMPEG)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            print("Could not open stream:", self.stream_url)
        else:
            print("Stream opened:", self.stream_url)
            threading.Thread(target=self._reader_loop, daemon=True).start()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(33, self._render_latest_frame)

    def _reader_loop(self):
        """Read frames in background so GUI never blocks."""
        while not self._stop.is_set():
            if self.cap is None:
                break

            ok, frame = self.cap.read()
            if not ok:
                # brief backoff; avoids tight loop when stream drops
                time.sleep(0.05)
                continue

            # BGR -> RGB
            self._latest_frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def _render_latest_frame(self):
        frame = self._latest_frame_rgb
        if frame is not None:
            w = self.preview.winfo_width()
            h = self.preview.winfo_height()
            if w > 10 and h > 10:
                frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(img)
            self._latest_imgtk = imgtk
            self.video_label.configure(image=imgtk)

        self.after(33, self._render_latest_frame)

    def on_close(self):
        self._stop.set()
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

    def on_move(self, direction):
        print("Move:", direction)


if __name__ == "__main__":
    app = MovieDirectorGUI()
    app.mainloop()