
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import threading
import time
import os
from datetime import datetime

import mediapipe
import cv2
import numpy

# Attempt socket programming
import socket
import pyaudio

import time
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision

# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    pose_landmark_style = drawing_styles.get_default_pose_landmarks_style()
    pose_connection_style = drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)

    for pose_landmarks in pose_landmarks_list:
        drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=pose_landmarks,
            connections=vision.PoseLandmarksConnections.POSE_LANDMARKS,
            landmark_drawing_spec=pose_landmark_style,
            connection_drawing_spec=pose_connection_style
        )

    return annotated_image


CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"

# !! Change into the Robot's IP when testing with the group5 SD card
SERVER_HOST = "172.17.10.222"
SERVER_PORT = 5001

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MovieDirectorGUI(ctk.CTk):
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket

        self.title("Movie Director Miniature")
        self.geometry("1000x650")
        self.minsize(850, 560)

        # Speed of the robot
        self.speed = 90

        # For video streaming
        self.stream_url = "http://172.17.10.222:8080/stream.mjpg"
        project_dir = os.path.dirname(os.path.abspath(__file__))

        # ---- Recording setup ----
        self.recordings_dir = os.path.join(project_dir, "recordings")
        os.makedirs(self.recordings_dir, exist_ok=True)

        self.is_recording = False
        self.record_start_time = None
        self.video_writer = None
        self.recording_filename = None
        self.record_fps = 20.0
        self.record_size = None

        # ---- Audio streaming ----
        self.setSpeaker = False
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )

        # For Autofocus
        self.setAfManual = False

        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Left
        self.left = ctk.CTkFrame(self, corner_radius=16)
        self.left.grid(row=0, column=0, padx=(18, 10), pady=(18, 10), sticky="ns")

        self.showZoom = False
        self.current_zoomvalue = 1

        left_icons = [
            "icons/camera.png",
            "icons/focus2.png",
            "icons/zoom.png",
            "icons/autofocus.png",
            "icons/colorFilter.png",
            "icons/joystick.png",
            "icons/lock.png"
        ]
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

        right_icons = [
            "icons/goldenratio2.png",
            "icons/icon2.png",
            "icons/icon3.png",
            "icons/rule-of-thirds.png",
            "icons/center.png"
        ]
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

        # ---- Recording overlays ----
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

        self.zoom_slider = ctk.CTkSlider(
            self.center,
            from_=1,
            to=8,
            number_of_steps=100,
            command=self.zoom_value
        )
        self.zoom_slider.set(self.current_zoomvalue)

        self.AF_slider = ctk.CTkSlider(
            self.center,
            from_=0,
            to=10,
            command=self.AfManual
        )
        self.AF_slider.set(0)

        # Add color filters
        self.colorFilterControls = ctk.CTkFrame(self.center, corner_radius=16)
        self.colorFilterControls.place(relx=250, rely=20)

        ctk.CTkButton(
            self.colorFilterControls,
            text="RGGB",
            width=52,
            height=52,
            corner_radius=14,
            command=lambda: self.on_right_action(0),
        ).place(relx=2, rely=2)

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

        try:
            rotate_left_icon_path = os.path.join(project_dir, "icons/rotateLeft.png")
            rotate_left_icon_img = Image.open(rotate_left_icon_path)
            rotate_left_icon_img = rotate_left_icon_img.resize((24, 24), Image.Resampling.LANCZOS)
            rotate_left_icon_photo = ImageTk.PhotoImage(rotate_left_icon_img)
            self.rotate_left_icon_photo = rotate_left_icon_photo

            ctk.CTkButton(
                self.dpad,
                text="",
                image=rotate_left_icon_photo,
                width=44,
                height=44,
                corner_radius=14,
                command=lambda: self.on_move("rotate left"),
            ).grid(row=0, column=0, padx=6, pady=6, sticky="nsew")
        except Exception as e:
            print(f"Error loading rotate left icon: {e}")
            ctk.CTkButton(
                self.dpad,
                text="",
                width=44,
                height=44,
                corner_radius=14,
                command=lambda: self.on_move("rotate left"),
            ).grid(row=0, column=0, padx=6, pady=6, sticky="nsew")

        try:
            rotate_right_icon_path = os.path.join(project_dir, "icons/rotateRight.png")
            rotate_right_icon_img = Image.open(rotate_right_icon_path)
            rotate_right_icon_img = rotate_right_icon_img.resize((24, 24), Image.Resampling.LANCZOS)
            rotate_right_icon_photo = ImageTk.PhotoImage(rotate_right_icon_img)
            self.rotate_right_icon_photo = rotate_right_icon_photo

            ctk.CTkButton(
                self.dpad,
                text="",
                image=rotate_right_icon_photo,
                width=44,
                height=44,
                corner_radius=14,
                command=lambda: self.on_move("rotate right"),
            ).grid(row=0, column=2, padx=6, pady=6, sticky="nsew")
        except Exception as e:
            print(f"Error loading rotate right icon: {e}")
            ctk.CTkButton(
                self.dpad,
                text="",
                width=44,
                height=44,
                corner_radius=14,
                command=lambda: self.on_move("rotate right"),
            ).grid(row=0, column=2, padx=6, pady=6, sticky="nsew")

        dpad_btn("▲", "up", 0, 1)
        dpad_btn("◀", "left", 1, 0)
        dpad_btn("●", "stand", 1, 1)
        dpad_btn("▶", "right", 1, 2)
        dpad_btn("▼", "down", 2, 1)
        dpad_btn("-", "-", 2, 0)
        dpad_btn("+", "+", 2, 2)

        # Look Up - Down Controls
        self.look = ctk.CTkFrame(self.bottom, corner_radius=16)
        self.look.grid(row=0, column=1, padx=1, pady=12, sticky="ew")

        try:
            look_up_path = os.path.join(project_dir, "icons/look-up.png")
            lookup_img = Image.open(look_up_path)
            lookup_img = lookup_img.resize((40, 40), Image.Resampling.LANCZOS)
            lookup_photo = ImageTk.PhotoImage(lookup_img)
            self.lookup_photo = lookup_photo

            ctk.CTkButton(
                self.look,
                image=lookup_photo,
                text="",
                width=52,
                height=52,
                corner_radius=14,
                command=lambda: self.on_move("look up"),
            ).pack(pady=6)
        except Exception as e:
            print(f"Error loading look up image: {e}")
            ctk.CTkButton(
                self.look,
                text="-",
                width=52,
                height=52,
                corner_radius=14,
                text_color="white",
                command=lambda: self.on_move("look up"),
            ).pack(pady=6)

        try:
            lookdown_path = os.path.join(project_dir, "icons/look-down.png")
            lookdown_img = Image.open(lookdown_path)
            lookdown_img = lookdown_img.resize((40, 40), Image.Resampling.LANCZOS)
            lookdown_photo = ImageTk.PhotoImage(lookdown_img)
            self.lookdown_photo = lookdown_photo

            ctk.CTkButton(
                self.look,
                image=lookdown_photo,
                text="",
                width=52,
                height=52,
                corner_radius=14,
                command=lambda: self.on_move("look down"),
            ).pack(pady=6)
        except Exception as e:
            print(f"Error loading look down image: {e}")
            ctk.CTkButton(
                self.look,
                text="-",
                width=52,
                height=52,
                corner_radius=14,
                command=lambda: self.on_move("look down"),
            ).pack(pady=6)

        # ---- Record Controls (middle) ----
        self.controls = ctk.CTkFrame(self.bottom, corner_radius=16)
        self.controls.grid(row=0, column=2, padx=24, pady=12, sticky="ew")

        try:
            record_path = os.path.join(project_dir, "icons/record.png")
            record_img = Image.open(record_path)
            record_img = record_img.resize((40, 40), Image.Resampling.LANCZOS)
            record_photo = ImageTk.PhotoImage(record_img)
            self.record_photo = record_photo

            self.record_button = ctk.CTkButton(
                self.controls,
                image=record_photo,
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

        try:
            pause_path = os.path.join(project_dir, "icons/pause.png")
            pause_img = Image.open(pause_path)
            pause_img = pause_img.resize((40, 40), Image.Resampling.LANCZOS)
            pause_photo = ImageTk.PhotoImage(pause_img)
            self.pause_photo = pause_photo

            self.pause_button = ctk.CTkButton(
                self.controls,
                image=pause_photo,
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

        try:
            stop_path = os.path.join(project_dir, "icons/stop.png")
            stop_img = Image.open(stop_path)
            stop_img = stop_img.resize((40, 40), Image.Resampling.LANCZOS)
            stop_photo = ImageTk.PhotoImage(stop_img)
            self.stop_photo = stop_photo

            self.stop_button = ctk.CTkButton(
                self.controls,
                image=stop_photo,
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

        # ---- Gallery, Speaker, Settings (right) ----
        self.utility = ctk.CTkFrame(self.bottom, corner_radius=16)
        self.utility.grid(row=0, column=3, padx=12, pady=12, sticky="e")

        try:
            gallery_path = os.path.join(project_dir, "icons/gallery.png")
            gallery_img = Image.open(gallery_path)
            gallery_img = gallery_img.resize((40, 40), Image.Resampling.LANCZOS)
            gallery_photo = ImageTk.PhotoImage(gallery_img)
            self.gallery_photo = gallery_photo

            self.gallery_button = ctk.CTkButton(
                self.utility,
                image=gallery_photo,
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

        try:
            speaker_path = os.path.join(project_dir, "icons/speaker.png")
            speaker_img = Image.open(speaker_path)
            speaker_img = speaker_img.resize((40, 40), Image.Resampling.LANCZOS)
            speaker_photo = ImageTk.PhotoImage(speaker_img)
            self.speaker_photo = speaker_photo

            speaker = ctk.CTkButton(
                self.utility,
                image=speaker_photo,
                text="",
                width=45,
                height=45,
                corner_radius=14,
                command=self.directorSpeaker
            )
            speaker.pack(side="left", padx=6)
        except Exception as e:
            print(f"Error loading speaker image: {e}")
            speaker = ctk.CTkButton(
                self.utility,
                text="🔊",
                width=52,
                height=52,
                corner_radius=14,
                command=self.directorSpeaker
            )
            speaker.pack(side="left", padx=6)

        try:
            settings_path = os.path.join(project_dir, "icons/settings.png")
            settings_img = Image.open(settings_path)
            settings_img = settings_img.resize((40, 40), Image.Resampling.LANCZOS)
            settings_photo = ImageTk.PhotoImage(settings_img)
            self.settings_photo = settings_photo

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

        # Initialize PoseLandmarker once
        base_options = python.BaseOptions(model_asset_path='pose_landmarker_full.task')
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=False
        )
        self.pose_detector = vision.PoseLandmarker.create_from_options(options)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(33, self._render_latest_frame)
        self.after(250, self._update_recording_timer)

        # --- Director Speaker stream state ---
        self.send_audio_event = threading.Event()
        threading.Thread(target=self.audio_sender, daemon=True).start()

        self.speed_label = ctk.CTkLabel(
            self.utility,
            text=str(self.speed),
            font=("Arial", 32)
        )
        self.speed_label.pack(side="left", padx=6)

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
        image = self._latest_frame_rgb

        if image is not None:
            w = self.preview.winfo_width()
            h = self.preview.winfo_height()
            if w > 10 and h > 10:
                image = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
            detection_result = self.pose_detector.detect(mp_image)

            self.process_result(detection_result, w, h)

            annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), detection_result)

            cv2.line(annotated_image, (int(w / 5), 0), (int(w / 5), h), (0, 255, 0), 3)
            cv2.line(annotated_image, (int(w / 5) * 2, 0), (int(w / 5) * 2, h), (0, 255, 0), 3)
            cv2.line(annotated_image, (int(w / 5) * 3, 0), (int(w / 5) * 3, h), (0, 255, 0), 3)
            cv2.line(annotated_image, (int(w / 5) * 4, 0), (int(w / 5) * 4, h), (0, 255, 0), 3)

            annotated_image_pil = Image.fromarray(annotated_image)
            annotated_imgtk = ImageTk.PhotoImage(annotated_image_pil)

            self._latest_imgtk = annotated_imgtk
            self.video_label.configure(image=annotated_imgtk)
            self.video_label.image = annotated_imgtk

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
        self.recording_filename = os.path.join(
            self.recordings_dir,
            f"recording_{timestamp}.avi"
        )

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

    def on_close(self):
        self._stop.set()

        if self.is_recording:
            self.stop_recording()

        try:
            if self.cap is not None:
                self.cap.release()
        finally:
            try:
                self.stream.stop_stream()
                self.stream.close()
                self.p.terminate()
            except Exception:
                pass
            self.destroy()

    # callbacks
    def on_left_action(self, idx):
        print("Left button", idx)

        if idx == 2:  # Zoom button
            self.showZoom = not self.showZoom
            if self.showZoom:
                self.zoom_slider.place(relx=0.5, rely=0.9, relwidth=0.7, relheight=0.06, anchor='center')
                print("open zoom slider")
            else:
                print("close zoom slider")
                self.zoom_slider.place_forget()

        if idx == 3:  # Autofocus
            self.setAfManual = not self.setAfManual
            if self.setAfManual:
                print("open autofocus slider")
                self.AF_slider.place(relx=0.5, rely=0.9, relwidth=0.7, relheight=0.06, anchor='center')
            else:
                print("close autofocus slider")
                self.AF_slider.place_forget()

    def AfManual(self, value):
        time.sleep(0.05)
        print("Lens position: ", value)
        self.sendMessage(f"autofocus:{value}")

    def process_result(self, detection_result, w, h):
        get_body = detection_result.pose_landmarks
        points = []

        if len(get_body) == 0:
            return

        result = get_body[0]
        right_sx = float(result[12].x * w)
        points.append(right_sx)

        left_sx = float(result[11].x * w)
        points.append(left_sx)

        right_hx = float(result[24].x * w)
        points.append(right_hx)

        left_hx = float(result[23].x * w)
        points.append(left_hx)

        # your tracking logic can stay here if you want to re-enable it later

    def on_right_action(self, idx):
        print("Right button", idx)

    def zoom_value(self, value):
        time.sleep(0.05)
        print("Zoom: ", value)
        state = "+"
        if value < self.current_zoomvalue:
            state = "-"
        self.current_zoomvalue = value
        self.sendMessage(f"zoom:{value}:{state}")

    def on_move(self, direction):
        print("Move:", direction)
        self.sendMessage(f"move:{direction}")

        if direction == "+":
            self.speed += 5
            self.speed_label.configure(text=str(self.speed))
        elif direction == "-":
            self.speed -= 5
            self.speed_label.configure(text=str(self.speed))

    def directorSpeaker(self):
        self.setSpeaker = not self.setSpeaker
        print(f"set speaker: {self.setSpeaker}")

        if self.send_audio_event.is_set():
            self.send_audio_event.clear()
        else:
            self.send_audio_event.set()

    def audio_sender(self):
        print("Audio thread started")

        while True:
            try:
                data = self.stream.read(CHUNK - 4, exception_on_overflow=False)

                if self.send_audio_event.is_set():
                    try:
                        self.client_socket.sendall(data)
                    except Exception as e:
                        print("Audio send error:", e)
                        break
            except Exception as e:
                print("Audio read error:", e)
                break

    def sendMessage(self, message):
        if not message:
            return

        try:
            self.client_socket.sendall(message.encode("utf-8"))
        except Exception as e:
            print(f"Error found while sending the message: {e}")


def start_client():
    """Start the client and connect to the server."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            app = MovieDirectorGUI(client_socket)
            app.mainloop()

    except ConnectionRefusedError:
        print(f"Connection to {SERVER_HOST}:{SERVER_PORT} failed. Ensure the server is running.")

    except Exception as e:
        print(f"An error occurred while running the application: {e}")
        print("You are forced to leave the chatroom... Please retry and come back again")


if __name__ == "__main__":
    start_client()