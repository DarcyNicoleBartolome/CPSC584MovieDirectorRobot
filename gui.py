import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import threading
import time

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