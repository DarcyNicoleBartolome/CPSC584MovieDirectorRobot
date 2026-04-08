
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
import os
from datetime import datetime

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
from mediapipe.tasks import python

# Draw the body landmarks for debugging
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
            connection_drawing_spec=pose_connection_style)
        
    return annotated_image

# Constant for audio processing
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"

# !! Change into the Robot's IP when testing with the group5 SD card
# SERVER_HOST = "172.17.10.222" # Raspy's with CPSC584 wifi
# SERVER_HOST = "172.17.10.159" # Raspy's with CPSC584 wifi
SERVER_HOST = "localhost" # localhost
SERVER_PORT = 5001
AUD_PORT = 5002

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MovieDirectorGUI(ctk.CTk):
    def __init__(self, client_socket, aud_socket):
        super().__init__()
        self.client_socket = client_socket
        self.aud_socket = aud_socket
        
        self.title("Movie Director Miniature")
        self.geometry("1000x650")
        self.minsize(850, 560)

        # Speed of the robot
        self.speed = 90

        # For video streaming
        # self.stream_url = "http://172.17.10.222:8080/stream.mjpg"
        self.stream_url = "http://localhost:8080/stream.mjpg"
        project_dir = os.path.dirname(os.path.abspath(__file__))

        # ---- Recording setup ----
        self.recordings_dir = os.path.join(project_dir, "recordings")
        os.makedirs(self.recordings_dir, exist_ok=True)

        self.is_recording = False
        self.is_paused = False
        self.record_start_time = None
        self.record_elapsed = 0.0
        self.video_writer = None
        self.recording_filename = None
        self.record_fps = 20.0
        self.record_size = None

        # ---- Audio streaming ----
        self.setSpeaker = False
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Left
        self.left = ctk.CTkFrame(self, corner_radius=16)
        self.left.grid(row=0, column=0, padx=(18, 10), pady=(18, 10), sticky="ns")

        # States for each buttons
        self.showZoom = False
        self.showCameraShots = False
        self.showGoldenRatio = False
        self.showCenterSymmetry = False
        self.showRuleofThirds = False
        self.current_zoomvalue = 1
        
        # auto tracking states
        self.manualMove = True
        self.forwardTrucking = False
        self.backwardTrucking = False
        self.tracking = False
        self.rotate_track = False
        self.symmetry = False
        self.ruleofthirds = False
        
        self.showTrackingOptions = False
        self.showTruckingOptions = False
        
        
        # Left side icons: camera, focus, zoom
        left_icons = ["icons/camera.png", 
                      "icons/zoom.png", 
                      "icons/tracking.png", 
                      "icons/trucking.png"]
        
        left_photos = []
        self.left_buttons = []
        

        # left_icons = [
        #     "icons/camera.png",
        #     "icons/focus2.png",
        #     "icons/zoom.png",
        #     "icons/autofocus.png",
        #     "icons/colorFilter.png",
        #     "icons/joystick.png",
        #     "icons/lock.png"
        # ]

        """Set up the left buttons"""
        for i, icon in enumerate(left_icons):
            try:
                icon_path = os.path.join(project_dir, icon)
                icon_img = Image.open(icon_path)
                icon_img = icon_img.resize((40, 40), Image.Resampling.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon_img)
                left_photos.append(icon_photo)
                
                left_button = ctk.CTkButton(
                    self.left, 
                    image=icon_photo,
                    text="",
                    width=52, 
                    height=52, 
                    corner_radius=14
                )
                
                left_button.configure(command=lambda btn=left_button, idx=i: self.on_left_action(idx, btn))
                left_button.grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))
                
            except Exception as e:
                print(f"Error loading {icon}: {e}")
                
                left_button = ctk.CTkButton(
                    self.left, 
                    text="",
                    width=52,
                    height=52,
                    corner_radius=14,
                    command=lambda idx=i: self.on_left_action(idx, left_button),
                )
                
                left_button.configure(command=lambda btn=left_button, idx=i: self.on_left_action(idx, btn))
                left_button.grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))
                
            self.left_buttons.append(left_button)
        
        self.left_photos = left_photos  # Keep references


        # Right
        self.right = ctk.CTkFrame(self, corner_radius=16)
        self.right.grid(row=0, column=2, padx=(10, 18), pady=(18, 10), sticky="ns")
        
        # Right side icons
        right_icons = [
            "icons/goldenratio2.png", 
            "icons/dolly.png", 
            "icons/dolly.png", 
            "icons/rule-of-thirds.png", 
            "icons/center.png"]
        right_photos = []
        self.right_buttons = []

        # Set up right buttons
        for i, icon in enumerate(right_icons):
            text = ""
            try:
                icon_path = os.path.join(project_dir, icon)
                icon_img = Image.open(icon_path)
                icon_img = icon_img.resize((40, 40), Image.Resampling.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon_img)
                right_photos.append(icon_photo)
                
                if i == 1:
                    text="In"
                elif i == 2:
                    text="Out"
                
                right_button = ctk.CTkButton(
                    self.right, 
                    image=icon_photo,
                    text=text,
                    width=52, 
                    height=52, 
                    corner_radius=14,
                    compound = "top",
                    command=lambda idx=i: self.on_right_action(idx, right_button),
                )
                
                right_button.configure(command=lambda btn=right_button, idx=i: self.on_right_action(idx, btn))
                right_button.grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))
                
            except Exception as e:
                print(f"Error loading {icon}: {e}")
                right_button = ctk.CTkButton(
                    self.right, 
                    text="",
                    width=52,
                    height=52,
                    corner_radius=14,
                    command=lambda idx=i: self.on_right_action(idx, right_button),
                )
                
                right_button.configure(command=lambda btn=right_button, idx=i: self.on_right_action(idx, btn))
                right_button.grid(row=i, column=0, padx=12, pady=(12 if i == 0 else 10, 0))
            
            self.right_buttons.append(right_button)
        
        self.right_photos = right_photos  # Keep references

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
        
        # ---- Select tracking options ----
        self.tracking_options = ctk.CTkFrame(self.center, corner_radius=12)

        self.sideway_tracking = ctk.CTkButton(
            self.tracking_options,
            text="Sideways",
            width=80,
            height=36,
            corner_radius=10,
            command=lambda: self.set_tracking("Sideways"),
        )
        self.sideway_tracking.pack(side="left", padx=6, pady=6)

        self.rotate_tracking = ctk.CTkButton(
            self.tracking_options,
            text="Rotate",
            width=80,
            height=36,
            corner_radius=10,
            command=lambda: self.set_tracking("Rotate"),
        )
        self.rotate_tracking.pack(side="left", padx=6, pady=6)
        
        # ---- Select trucking options ----
        self.trucking_options = ctk.CTkFrame(self.center, corner_radius=12)

        self.forward_trucking = ctk.CTkButton(
            self.trucking_options,
            text="Forward",
            width=80,
            height=36,
            corner_radius=10,
            command=lambda: self.set_trucking("Forward"),
        )
        self.forward_trucking.pack(side="left", padx=6, pady=6)

        self.backward_trucking = ctk.CTkButton(
            self.trucking_options,
            text="Back",
            width=80,
            height=36,
            corner_radius=10,
            command=lambda: self.set_trucking("Back"),
        )
        self.backward_trucking.pack(side="left", padx=6, pady=6)
        
        
        # Set up the zoom slider place in the bottom of the preview screen
        self.zoom_slider = ctk.CTkSlider(
            self.center,
            from_=1,
            to=8,
            number_of_steps=100,
            command=self.zoom_value
        )
        self.zoom_slider.set(self.current_zoomvalue)

        # ---- Camera shot presets ----
        self.camera_shots_frame = ctk.CTkFrame(self.center, corner_radius=12, fg_color="gray20")

        ctk.CTkButton(
            self.camera_shots_frame,
            text="Wide",
            width=80,
            height=36,
            corner_radius=10,
            command=lambda: self.set_camera_shot("wide"),
        ).pack(side="left", padx=6, pady=6)

        ctk.CTkButton(
            self.camera_shots_frame,
            text="Mid",
            width=80,
            height=36,
            corner_radius=10,
            command=lambda: self.set_camera_shot("mid"),
        ).pack(side="left", padx=6, pady=6)

        ctk.CTkButton(
            self.camera_shots_frame,
            text="Close Up",
            width=80,
            height=36,
            corner_radius=10,
            command=lambda: self.set_camera_shot("closeup"),
        ).pack(side="left", padx=6, pady=6)

        # Add color filters
        # self.colorFilterControls = ctk.CTkFrame(self.center, corner_radius=16)
        # self.colorFilterControls.place(relx=250, rely=20)

        # ctk.CTkButton(
        #     self.colorFilterControls,
        #     text="RGGB",
        #     width=52,
        #     height=52,
        #     corner_radius=14,
        #     command=lambda: self.on_right_action(0),
        # ).place(relx=2, rely=2)

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
        self.record_section = ctk.CTkFrame(self.bottom, corner_radius=16, fg_color="transparent")
        self.record_section.grid(row=0, column=2, padx=24, pady=12, sticky="ew")

        self.controls = ctk.CTkFrame(self.record_section, corner_radius=16)
        self.controls.pack()

        # Video name entry
        self.video_name_entry = ctk.CTkEntry(
            self.record_section,
            placeholder_text="Enter video name",
            width=200,
            height=30,
            corner_radius=10,
        )
        self.video_name_entry.pack(pady=(6, 0))

        self.video_name_error = ctk.CTkLabel(
            self.record_section,
            text="",
            text_color="#FF4444",
            font=("Arial", 12),
        )
        self.video_name_error.pack(pady=(2, 0))

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
                command=self.pause_recording,
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
                command=self.pause_recording,
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

        self.is_dark_mode = True

        try:
            bulb_path = os.path.join(project_dir, "icons/bulb.png")
            bulb_img = Image.open(bulb_path)
            bulb_img = bulb_img.resize((40, 40), Image.Resampling.LANCZOS)
            bulb_photo = ImageTk.PhotoImage(bulb_img)
            self.bulb_photo = bulb_photo

            ctk.CTkButton(
                self.utility,
                image=bulb_photo,
                text="",
                width=45,
                height=45,
                corner_radius=14,
                command=self.toggle_theme,
            ).pack(side="left", padx=6)
        except Exception as e:
            print(f"Error loading bulb image: {e}")
            ctk.CTkButton(
                self.utility,
                text="💡",
                width=52,
                height=52,
                corner_radius=14,
                command=self.toggle_theme,
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
            self.after(3000, lambda:self.set_status(""))
            threading.Thread(target=self._reader_loop, daemon=True).start()

        # Initialize PoseLandmarker once
        base_options = python.BaseOptions(model_asset_path='pose_landmarker_lite.task')
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            min_pose_detection_confidence = 0.5,
            min_pose_presence_confidence=0.5,
            output_segmentation_masks=False)
        self.pose_detector = vision.PoseLandmarker.create_from_options(options)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(33, self._render_latest_frame)
        self.after(250, self._update_recording_timer)

        # --- Director Speaker stream state ---
        self.send_audio_event = threading.Event()
        threading.Thread(target=self.audio_sender, daemon=True).start()
        
        self.send_zoom_event = threading.Event()
        threading.Thread(target=self.zoom_value, daemon=True).start()
        
        
        
        # !! ROBOT SPEED CHANGE POSITION LATER
        self.speed_label = ctk.CTkLabel(
            self.utility,
            text=str(self.speed),
            font=("Arial", 32)
        )
        self.speed_label.pack(side="left", padx=6)

    def set_status(self, message):
        self.status_label.configure(text=message)
        if message:
            self.status_label.place(relx=0.5, rely=0.10, anchor="n")
        else:
            self.status_label.place_forget()

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

            if self.is_recording and not self.is_paused and self.video_writer is not None:
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

            # annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), detection_result)
            annotated_image = np.copy(mp_image.numpy_view())

            if self.showGoldenRatio:
                annotated_image = self._draw_golden_spiral(annotated_image, w, h)

            if self.showCenterSymmetry:
                annotated_image = self._draw_center_symmetry(annotated_image, w, h)
                
            if self.showRuleofThirds:
                annotated_image = self._draw_rule_of_thirds(annotated_image, w, h)

            # Convert to PhotoImage for Tkinter display
            annotated_image_pil = Image.fromarray(annotated_image)
            annotated_imgtk = ImageTk.PhotoImage(annotated_image_pil)
            
            

            self._latest_imgtk = annotated_imgtk
            self.video_label.configure(image=annotated_imgtk)
            # self.video_label.image = annotated_imgtk 

        self.after(33, self._render_latest_frame)

    def _update_recording_timer(self):
        if self.is_recording and self.record_start_time is not None:
            if self.is_paused:
                elapsed = int(self.record_elapsed)
            else:
                elapsed = int(self.record_elapsed + (time.time() - self.record_start_time))
            mins = elapsed // 60
            secs = elapsed % 60
            if self.is_paused:
                self.timer_label.configure(text=f"⏸ PAUSED  {mins:02d}:{secs:02d}", fg_color="#8B8000")
            else:
                self.timer_label.configure(text=f"● REC  {mins:02d}:{secs:02d}", fg_color="#8B0000")
            self.timer_label.place(relx=0.5, rely=0.03, anchor="n")
        else:
            self.timer_label.place_forget()

        self.after(250, self._update_recording_timer)

    def start_recording(self):
        if self.is_recording:
            self.set_status("Already recording")
            return

        video_name = self.video_name_entry.get().strip()
        if not video_name:
            self.video_name_error.configure(text="No video name, please enter")
            return

        self.video_name_error.configure(text="")

        filepath = os.path.join(self.recordings_dir, f"{video_name}.avi")
        if os.path.exists(filepath):
            self.video_name_error.configure(text="Video name already exists, please choose another name")
            return

        if self._latest_frame_bgr is None:
            self.set_status("No video frame available yet")
            return

        frame = self._latest_frame_bgr
        h, w = frame.shape[:2]
        self.record_size = (w, h)

        self.recording_filename = filepath

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
        self.is_paused = False
        self.record_elapsed = 0.0
        self.record_start_time = time.time()
        self.video_name_entry.delete(0, "end")
        self.set_status("Recording started")
        print("Recording started:", self.recording_filename)
        self.after(3000, lambda:self.set_status(""))

    def stop_recording(self):
        if not self.is_recording:
            self.set_status("Not currently recording")
            return

        self.is_recording = False
        self.is_paused = False
        self.record_start_time = None
        self.record_elapsed = 0.0

        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None

        saved_name = os.path.basename(self.recording_filename) if self.recording_filename else "video"
        self.set_status(f"Saved: {saved_name}")
        self.after(3000, lambda: self.set_status(""))
        print("Stopped recording:", self.recording_filename)

    def pause_recording(self):
        if not self.is_recording:
            self.set_status("Not currently recording")
            return

        if self.is_paused:
            # Resume: restart the segment timer
            self.is_paused = False
            self.record_start_time = time.time()
            self.set_status("Recording resumed")
            print("Recording resumed")
        else:
            # Pause: accumulate elapsed time from the current segment
            self.record_elapsed += time.time() - self.record_start_time
            self.is_paused = True
            self.set_status("Recording paused")
            print("Recording paused")

    def get_recordings(self):
        files = []
        for f in os.listdir(self.recordings_dir):
            if f.lower().endswith((".avi", ".mp4", ".mov", ".mkv")):
                files.append(f)
        files.sort(reverse=True)
        return files

    def open_gallery(self):
        gallery = ctk.CTkToplevel(self)
        gallery.title("Gallery")
        gallery.geometry("500x400")

        ctk.CTkLabel(gallery, text="Saved Recordings", font=("Arial", 20, "bold")).pack(pady=12)

        gallery_status = ctk.CTkLabel(gallery, text="", font=("Arial", 13))
        gallery_status.pack(pady=(0, 4))

        scroll = ctk.CTkScrollableFrame(gallery, width=440, height=260)
        scroll.pack(padx=12, pady=12, fill="both", expand=True)

        def show_gallery_status(msg):
            gallery_status.configure(text=msg)
            gallery.after(2000, lambda: gallery_status.configure(text=""))

        def refresh_gallery():
            for widget in scroll.winfo_children():
                widget.destroy()

            files = self.get_recordings()
            if not files:
                ctk.CTkLabel(scroll, text="No recordings found").pack(pady=10)
                return

            for filename in files:
                row = ctk.CTkFrame(scroll)
                row.pack(fill="x", padx=6, pady=6)

                ctk.CTkLabel(row, text=filename, anchor="w").pack(side="left", padx=8, pady=8)

                ctk.CTkButton(
                    row,
                    text="Delete",
                    width=70,
                    fg_color="#CC0000",
                    hover_color="#990000",
                    command=lambda f=filename: delete_recording(f)
                ).pack(side="right", padx=4, pady=8)

                ctk.CTkButton(
                    row,
                    text="Play",
                    width=80,
                    command=lambda f=filename: self.play_recording(os.path.join(self.recordings_dir, f))
                ).pack(side="right", padx=4, pady=8)

        def delete_recording(filename):
            filepath = os.path.join(self.recordings_dir, filename)
            try:
                os.remove(filepath)
                show_gallery_status(f"Deleted: {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {e}")
                show_gallery_status(f"Failed to delete: {filename}")
            refresh_gallery()

        refresh_gallery()

    def play_recording(self, filepath):
        player = ctk.CTkToplevel(self)
        player.title(os.path.basename(filepath))
        player.geometry("800x580")

        video_frame = ctk.CTkLabel(player, text="")
        video_frame.pack(fill="both", expand=True, padx=10, pady=(10, 4))

        cap = cv2.VideoCapture(filepath)

        if not cap.isOpened():
            ctk.CTkLabel(player, text="Failed to open video").pack(pady=10)
            return

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
        total_seconds = total_frames / fps if fps > 0 else 0
        frame_delay = int(1000 / fps) if fps > 0 else 33

        state = {
            "playing": True,
            "seeking": False,
            "speed": 1.0,
        }

        # --- Seek bar ---
        seek_slider = ctk.CTkSlider(
            player, from_=0, to=max(total_frames - 1, 1), number_of_steps=max(total_frames - 1, 1)
        )
        seek_slider.set(0)
        seek_slider.pack(fill="x", padx=16, pady=(4, 2))

        def on_seek_press(event):
            state["seeking"] = True

        def on_seek_release(event):
            frame_no = int(seek_slider.get())
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            state["seeking"] = False
            if not state["playing"]:
                show_frame_at_current_pos()

        seek_slider.bind("<ButtonPress-1>", on_seek_press)
        seek_slider.bind("<ButtonRelease-1>", on_seek_release)

        # --- Controls row ---
        controls_frame = ctk.CTkFrame(player, corner_radius=12)
        controls_frame.pack(fill="x", padx=16, pady=(2, 10))

        def fmt_time(seconds):
            m = int(seconds) // 60
            s = int(seconds) % 60
            return f"{m:02d}:{s:02d}"

        time_label = ctk.CTkLabel(controls_frame, text=f"00:00 / {fmt_time(total_seconds)}", font=("Arial", 13))
        time_label.pack(side="right", padx=12)

        speed_label = ctk.CTkLabel(controls_frame, text="1.0x", font=("Arial", 13))
        speed_label.pack(side="right", padx=6)

        def toggle_play():
            state["playing"] = not state["playing"]
            if state["playing"] and state.get("pause_icon"):
                play_btn.configure(image=state["pause_icon"], text="")
            elif state.get("play_icon"):
                play_btn.configure(image=state["play_icon"], text="")
            else:
                play_btn.configure(image="", text="▶" if not state["playing"] else "⏸")
            if state["playing"]:
                update_video()

        def slower():
            state["speed"] = max(0.25, state["speed"] - 0.5)
            speed_label.configure(text=f"{state['speed']:.2g}x")

        def faster():
            state["speed"] = min(8.0, state["speed"] + 0.5)
            speed_label.configure(text=f"{state['speed']:.2g}x")

        btn_cfg = dict(width=44, height=36, corner_radius=10)

        # Load player control icons
        project_dir = os.path.dirname(os.path.abspath(__file__))
        icon_size = (24, 24)
        try:
            rw_img = Image.open(os.path.join(project_dir, "icons/rewind.png")).resize(icon_size, Image.Resampling.LANCZOS)
            state["rewind_icon"] = ImageTk.PhotoImage(rw_img)
        except Exception:
            state["rewind_icon"] = None
        try:
            fw_img = Image.open(os.path.join(project_dir, "icons/forward.png")).resize(icon_size, Image.Resampling.LANCZOS)
            state["forward_icon"] = ImageTk.PhotoImage(fw_img)
        except Exception:
            state["forward_icon"] = None
        try:
            pause2_img = Image.open(os.path.join(project_dir, "icons/pause2.png")).resize(icon_size, Image.Resampling.LANCZOS)
            state["pause_icon"] = ImageTk.PhotoImage(pause2_img)
        except Exception:
            state["pause_icon"] = None
        try:
            play_img = Image.open(os.path.join(project_dir, "icons/play.png")).resize(icon_size, Image.Resampling.LANCZOS)
            state["play_icon"] = ImageTk.PhotoImage(play_img)
        except Exception:
            state["play_icon"] = None

        if state["rewind_icon"]:
            ctk.CTkButton(controls_frame, image=state["rewind_icon"], text="", command=slower, **btn_cfg).pack(side="left", padx=4, pady=6)
        else:
            ctk.CTkButton(controls_frame, text="\u23ea", command=slower, **btn_cfg).pack(side="left", padx=4, pady=6)

        if state["pause_icon"]:
            play_btn = ctk.CTkButton(controls_frame, image=state["pause_icon"], text="", command=toggle_play, width=52, height=36, corner_radius=10)
        else:
            play_btn = ctk.CTkButton(controls_frame, text="\u23f8", command=toggle_play, width=52, height=36, corner_radius=10)
        play_btn.pack(side="left", padx=4, pady=6)

        if state["forward_icon"]:
            ctk.CTkButton(controls_frame, image=state["forward_icon"], text="", command=faster, **btn_cfg).pack(side="left", padx=4, pady=6)
        else:
            ctk.CTkButton(controls_frame, text="\u23e9", command=faster, **btn_cfg).pack(side="left", padx=4, pady=6)

        def show_frame_at_current_pos():
            if not player.winfo_exists():
                return
            ok, frame = cap.read()
            if ok:
                display_frame(frame)
                pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                if not state["seeking"]:
                    seek_slider.set(pos)
                current_sec = pos / fps if fps > 0 else 0
                time_label.configure(text=f"{fmt_time(current_sec)} / {fmt_time(total_seconds)}")

        def display_frame(frame):
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            w = max(video_frame.winfo_width(), 100)
            h = max(video_frame.winfo_height(), 100)
            frame_rgb = cv2.resize(frame_rgb, (w, h), interpolation=cv2.INTER_AREA)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(img)
            # video_frame.imgtk = imgtk # !!!
            video_frame.configure(image=imgtk)

        def update_video():
            if not player.winfo_exists():
                cap.release()
                return

            if not state["playing"]:
                return

            if state["seeking"]:
                player.after(frame_delay, update_video)
                return

            ok, frame = cap.read()
            if not ok:
                # End of video — stop playback
                state["playing"] = False
                if state.get("play_icon"):
                    play_btn.configure(image=state["play_icon"], text="")
                else:
                    play_btn.configure(image="", text="▶")
                return

            display_frame(frame)

            pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            seek_slider.set(pos)
            current_sec = pos / fps if fps > 0 else 0
            time_label.configure(text=f"{fmt_time(current_sec)} / {fmt_time(total_seconds)}")

            delay = max(1, int(frame_delay / state["speed"]))
            player.after(delay, update_video)

        def on_player_close():
            state["playing"] = False
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
    def on_left_action(self, idx, button):
        print("Left button", idx)
        
        if idx == 0:  # Camera shot presets
            was_open = self.showCameraShots
            self._close_all_overlays()
            if not was_open:
                self.showCameraShots = True
                self.camera_shots_frame.place(relx=0.5, rely=0.9, anchor='center')
                print("open camera shots")
            else:
                print("close camera shots")
        
        if idx == 1:  # Zoom button
            was_open = self.showZoom
            self._close_all_overlays()
            if not was_open:
                self.showZoom = True
                self.zoom_slider.place(relx=0.5, rely=0.9, relwidth=0.7, relheight=0.06, anchor='center')
                print("open zoom slider")
            else:
                print("close zoom slider")
         
        # Click button to show tracking options       
        elif idx == 2:
            self.showTrackingOptions = not self.showTrackingOptions
            self.toggleTrackingOptions()
            if self.showTrackingOptions:
                button.configure(fg_color="green")
                self.zoom_slider.place_forget()
                self.showZoom = False
                self.trucking_options.place_forget()
                self.tracking_options.place(relx=0.5, rely=0.9, anchor='center')
            else:
                button.configure(fg_color=("#3B8ED0", "#1F6AA5"))
                self.tracking_options.place_forget()
            
        # Click button to show trucking options 
        elif idx == 3: 
            self.showTruckingOptions = not self.showTruckingOptions
            self.toggleTruckingOptions()
            if self.showTruckingOptions:
                button.configure(fg_color="green")
                self.zoom_slider.place_forget()
                self.showZoom = False
                self.tracking_options.place_forget()
                self.trucking_options.place(relx=0.5, rely=0.9, anchor='center')
                
            else:
                button.configure(fg_color=("#3B8ED0", "#1F6AA5"))
                self.trucking_options.place_forget()

                
        self.updateLeftbutton(button, idx)
            
    def _close_all_overlays(self):
        """Close all center overlays (zoom, camera shots, AF slider)."""
        if self.showZoom:
            self.showZoom = False
            self.zoom_slider.place_forget()
        if self.showCameraShots:
            self.showCameraShots = False
            self.camera_shots_frame.place_forget()

    def set_camera_shot(self, shot_type):
        zoom_map = {"wide": 1.0, "mid": 3.0, "closeup": 6.0}
        zoom_val = zoom_map.get(shot_type, 1.0)

        state = "+" if zoom_val > self.current_zoomvalue else "-"
        self.current_zoomvalue = zoom_val
        self.zoom_slider.set(zoom_val)
        self.sendMessage(f"zoom:{zoom_val}:{state}")
        self.set_status(f"Camera: {shot_type.replace('closeup', 'close up')}")
        self.after(2000, lambda: self.set_status(""))
        print(f"Camera shot: {shot_type} -> zoom {zoom_val}")



    # Process the detection results to create robot tracking if any one of them is on
    def process_result(self, detection_result, w, h):
        get_body = detection_result.pose_landmarks
        points = []

        if len(get_body) == 0:
            return

        # Calculate shoulder and hip points to screen coordinates
        result = get_body[0]
        right_sx = float(result[12].x * w)
        points.append(right_sx)
        right_sy = float(result[12].y * h)
        
        left_sx = float(result[11].x * w)
        points.append(left_sx)
        left_sy = float(result[11].y * h)
        
        right_hx = float(result[24].x * w)
        points.append(right_hx)
        right_hy = float(result[24].y * h)
        
        left_hx = float(result[23].x * w)
        points.append(left_hx)
        left_hy = float(result[23].y * h)
        
        if not hasattr(self, "last_auto_time"):
            self.last_auto_time = 0
            self.last_direction = None

        now = time.time()
        if now - self.last_auto_time < 1.5:
            return
        
        # Determine the tracking based on the points only if any of the states are true
        
        if self.forwardTrucking:
            self.autoTrucking(left_sx, right_sx)
        elif self.tracking:
            self.autoTracking(points, w)
        elif self.backwardTrucking:
            self.autoBackwardtrucking(points, w)
        elif self.rotate_track:
            self.autoRotate(points, w)
        elif self.ruleofthirds:
            self.autoRuleofThirds(points, left_sx, right_sx, right_hx, left_hx, w)
        elif self.symmetry:
            self.autoSymmetry(right_sx, left_sx, w)
        
    
    # Robot moves sideways based on if subject is either at on one of the edges of the screen
    def autoTracking(self, list, w):
        if not hasattr(self, "last_auto_time"):
            self.last_auto_time = 0
            self.last_direction = None

        now = time.time()
        if now - self.last_auto_time < 1.5:
            return
        # Move left if atleast 2 points of the torso is at w/5 at the left of the screen
        if sum(1 for x in list if x < w/5) >= 2:
            self.sendMessage(f"move:left")
    
        # Move right if atleast 2 points of the torso is at w/5 at the right of the screen
        if sum(1 for x in list if x > w/5*4) >= 2:
            self.sendMessage(f"move:right")
                
    
    # Robot auto moves forward
    def autoTrucking(self, left_sx, right_sx):
        if not hasattr(self, "last_auto_time"):
            self.last_auto_time = 0
            self.last_direction = None

        now = time.time()
        if now - self.last_auto_time < 1.5:
            return
        # Move forward if shoulders are too far
        if (abs(left_sx-right_sx) < 100):
            self.sendMessage(f"move:up")
    
    # Robot auto moves backwards
    def autoBackwardtrucking(self, left_sx, right_sx):
        if not hasattr(self, "last_auto_time"):
            self.last_auto_time = 0
            self.last_direction = None

        now = time.time()
        if now - self.last_auto_time < 1.5:
            return
        # Move backward if shoulders are too close
        # print(abs(left_sx-right_sx))
        if (abs(left_sx-right_sx) > 120):
            self.sendMessage(f"move:down")
        
    # Auto Rotate robot if subject is at the end of one of the side of the screen
    def autoRotate(self, list, w):
        if not hasattr(self, "last_auto_time"):
            self.last_auto_time = 0
            self.last_direction = None

        now = time.time()
        if now - self.last_auto_time < 1.5:
            return
        # Move left if atleast 2 points of the torso is at w/5 at the left of the screen
        if sum(1 for x in list if x < w/5) >= 2:
            self.sendMessage(f"move:rotate left")
            time.sleep(1)
    
        # Move right if atleast 2 points of the torso is at w/5 at the right of the screen
        if sum(1 for x in list if x > w/5*4) >= 2:
            self.sendMessage(f"move:rotate right")
            time.sleep(1)
        
    # 
    def autoRuleofThirds(self, list, left_sx, right_sx, right_hx, left_hx, w):
        if not hasattr(self, "last_auto_time"):
            self.last_auto_time = 0
            self.last_direction = None

        now = time.time()
        if now - self.last_auto_time < 1.5:
            return
        mid_point_shoulder = abs((1-(1/2))*left_sx + (1/2)*right_sx)
        mid_point_hip = abs((1-(1/2))*left_hx + (1/2)*right_hx)
        
        # Move left if atleast 3 points of the torso is at w/5 at the left of the screen
        if sum(1 for x in list if x < (w/5) * 2) > 2:
            # Checks which torso is closer to one of the rule of thirds line (w/3)
            check_leftLine = max(0, min(100, (mid_point_shoulder * 3 / (1 * w)) * 100)) 
            check_rightLine = max(0, min(100, (mid_point_hip * 3 / (1 * w)) * 100)) 
            print("move:left", check_leftLine, check_rightLine)
            self.sendMessage("move:left")
            # while check_leftLine < 100 and check_rightLine < 100:
            #     print(check_leftLine, check_rightLine)
            #     self.sendMessage(f"move:left")
                
        elif sum(1 for x in list if x > (w/5) * 3) > 2:
            # Checks which torso is closer to one of the rule of thirds line (w/3)
            check_leftLine = max(0, min(100, ((w - mid_point_shoulder) / (1 * w / 3)) * 100))
            check_rightLine = max(0, min(100, ((w - mid_point_hip) / (1 * w / 3)) * 100))
            print("move:right",check_leftLine, check_rightLine)
            self.sendMessage("move:right")
            # while check_leftLine < 100 and check_rightLine < 100:
            #     print(check_leftLine, check_rightLine)
            #     self.sendMessage(f"move:right")
            
        elif sum(1 for x in list if x > (w/5) * 2 and x < (w/5) * 3) >= 2:
            print("subject on middle")
            if abs(mid_point_shoulder - (w/3)) < abs(mid_point_shoulder - (w/3) * 2):
                print("go left")
                self.sendMessage("move:left")
                # while 
            else:
                print("go right!")
                self.sendMessage("move:right")
                
        self.ruleofthirds = False
        
        
    # Calculate the center of attention based on teh subject
    def autoSymmetry(self, right_sx, left_sx, w):
        if not hasattr(self, "last_auto_time"):
            self.last_auto_time = 0
            self.last_direction = None

        now = time.time()
        if now - self.last_auto_time < 1.5:
            return
        if self.symmetry:
            shoulder_length = abs(left_sx-right_sx)
            
            percentage_rightShoulder = max(0, min(100, (right_sx * 2 / (1 * w)) * 100))
            percentage_leftShoulder = max(0, min(100, ((w - left_sx) / (1 * w / 2)) * 100))
            print(percentage_rightShoulder, percentage_leftShoulder)
            
            if percentage_rightShoulder < 70:
                self.sendMessage(f"move:left")
                print(f"move:left")
            elif percentage_leftShoulder < 70:
                self.sendMessage(f"move:right")
                print(f"move:right")
            
            self.symmetry = False
                
            time.sleep(2)
                

    def repeat_action(self, count, move_cmd, zoom_step):
        def step(i):
            if i >= count:
                return

            self.sendMessage(f"{move_cmd}\n")

            self.current_zoomvalue += zoom_step
            self.zoom_value(self.current_zoomvalue)
            self.zoom_slider.set(self.current_zoomvalue)

            # schedule next step (e.g., 50ms later)
            self.after(50, step, i + 1)

        step(0)
        

    def _draw_golden_spiral(self, image, w, h):
        overlay = image.copy()
        phi = 1.618
        color = (0, 215, 255)  # gold in BGR->RGB
        thickness = 2

        # !!!!
        # Starting rectangle
        # x, y = 0, 0
        # rw, rh = w, h
        scale = 1
        sw, sh = int(w * scale), int(h * scale)
        ox, oy = (w - sw) // 2, (h - sh) // 2
        x, y = ox, oy
        rw, rh = sw, sh

        for i in range(10):
            if i % 4 == 0:
                sq = int(rh)
                center = (x + sq, y + sq)
                cv2.ellipse(overlay, center, (sq, sq), 180, 0, 90, color, thickness, cv2.LINE_AA)
                x += sq
                rw -= sq
            elif i % 4 == 1:
                sq = int(rw)
                center = (x, y + sq)
                cv2.ellipse(overlay, center, (sq, sq), 0, 270, 360, color, thickness, cv2.LINE_AA)
                y += sq
                rh -= sq
            elif i % 4 == 2:
                sq = int(rh)
                center = (x - 1, y)
                cv2.ellipse(overlay, center, (sq, sq), 0, 0, 90, color, thickness, cv2.LINE_AA)
                rw -= sq
                x -= sq
            else:
                sq = int(rw)
                center = (x + sq, y)
                cv2.ellipse(overlay, center, (sq, sq), 0, 90, 180, color, thickness, cv2.LINE_AA)
                rh -= sq
                y -= sq

            if rw < 2 or rh < 2:
                break

        cv2.addWeighted(overlay, 0.6, image, 0.4, 0, image)
        return image

    
    def toggle_theme(self):
        """Toggle the dark / white theme of the gui"""
        self.is_dark_mode = not self.is_dark_mode
        mode = "dark" if self.is_dark_mode else "light"
        ctk.set_appearance_mode(mode)
        print(f"Theme changed to {mode}")
        
    def _draw_rule_of_thirds(self, image, w, h):
        # print("drawing rule of thirds")
        overlay = image.copy()
        
        # Rule of thirds intersection points
        cv2.circle(overlay, (int(w/3), int(h/3)), 15, (255, 0, 0), 10)
        cv2.circle(overlay, (int(w/3)*2, int(h/3)), 15, (255, 0, 0), 10)
        
        cv2.circle(overlay, (int(w/3), int(h/3)*2), 15, (255, 0, 0), 10)
        cv2.circle(overlay, (int(w/3)*2, int(h/3)*2), 15, (255, 0, 0), 10)
        
        # # Rule of thirds line
        cv2.line(overlay, (int(w/3), 0), (int(w/3), h), (0, 0, 255), 3)
        cv2.line(overlay, (int(w/3)*2, 0), (int(w/3)*2, h), (0, 0, 255), 3)
        cv2.line(overlay, (0, int(h/3)), (w, int(h/3)), (0, 0, 255), 3)
        cv2.line(overlay, (0, int(h/3)*2), (w, int(h/3)*2), (0, 0, 255), 3)
        
        cv2.addWeighted(overlay, 0.5, image, 0.5, 0, image)
        return image

    def _draw_center_symmetry(self, image, w, h):
        overlay = image.copy()
        color = (255, 255, 0)  # cyan-ish
        cx, cy = w // 2, h // 2

        # Vertical and horizontal center lines
        cv2.line(overlay, (cx, 0), (cx, h), color, 2, cv2.LINE_AA)
        cv2.line(overlay, (0, cy), (w, cy), color, 2, cv2.LINE_AA)

        # Center crosshair circle
        cv2.circle(overlay, (cx, cy), 20, color, 2, cv2.LINE_AA)
        cv2.circle(overlay, (cx, cy), 4, color, -1, cv2.LINE_AA)

        # Diagonal guides
        cv2.line(overlay, (0, 0), (w, h), color, 1, cv2.LINE_AA)
        cv2.line(overlay, (w, 0), (0, h), color, 1, cv2.LINE_AA)

        cv2.addWeighted(overlay, 0.5, image, 0.5, 0, image)
        return image

    def _close_all_composition_overlays(self):
        """Close all composition overlays (golden ratio, center symmetry)."""
        self.showGoldenRatio = False
        self.showCenterSymmetry = False
        self.showRuleofThirds = False


    def on_right_action(self, idx, button):
        # Pressing the Dolly In button
        if idx == 1:
            self.repeat_action(5, "move:up", -0.1)
        # Pressing the Dolly Out button
        elif idx == 2:
            self.repeat_action(5, "move:down", 0.1)
                
        # Adjust position by rule of thirds
        if idx == 3: # If rule of thirds is clicked
            self.ruleofthirds = not self.ruleofthirds
            was_on = self.showRuleofThirds
            self._close_all_composition_overlays()
            if not was_on:
                self.showRuleofThirds = True
            print(f"Rule of thirds overlay: {'on' if self.showRuleofThirds else 'off'}")
                
        # Adjust position by Center of attention
        if idx == 4: # Center of attention is clicked
            self.symmetry = not self.symmetry
            if self.symmetry:
                button.configure(fg_color="green")
            else:
                button.configure(fg_color=("#3B8ED0", "#1F6AA5"))
             
            
        print("Right button", idx)
        if idx == 0:  # Golden ratio
            was_on = self.showGoldenRatio
            self._close_all_composition_overlays()
            if not was_on:
                self.showGoldenRatio = True
            print(f"Golden ratio overlay: {'on' if self.showGoldenRatio else 'off'}")
        elif idx == 4:  # Center of symmetry
            was_on = self.showCenterSymmetry
            self._close_all_composition_overlays()
            if not was_on:
                self.showCenterSymmetry = True
            print(f"Center symmetry overlay: {'on' if self.showCenterSymmetry else 'off'}")
        else:
            self._close_all_composition_overlays()

    # Send the zoom value to the server to set the camera's zoom
    def zoom_value(self, value):
        time.sleep(0.05) # Add time sleep for proper processing
        print("Zoom: ", value)
        # decrease if zoom in or out based on camparing the current zoom value with the given value
        state = "+"
        if value < self.current_zoomvalue:
            state = "-"
        self.current_zoomvalue = value
        self.sendMessage(f"zoom:{value}:{state}\n")
        

    # Send the move command to the server to move the robot to a certain direction or change speed by 5
    def on_move(self, direction):
        print("Move:", direction)
        self.sendMessage(f"move:{direction}")

        # + increase speed by 5, - decrease speed by 5
        if direction == "+":
            self.speed += 5
            self.speed_label.configure(text=str(self.speed))
        elif direction == "-":
            self.speed -= 5
            self.speed_label.configure(text=str(self.speed))

    # toggle the speaker
    def directorSpeaker(self):
        self.setSpeaker = not self.setSpeaker
        print(f"set speaker: {self.setSpeaker}")
        
        if self.send_audio_event.is_set():
            self.send_audio_event.clear()
        else:
            self.send_audio_event.set()

    # Sends audio data to the server
    def audio_sender(self):
        print("Audio thread started")

        while True:
            data = self.stream.read(CHUNK, exception_on_overflow=False) #
            # Only send when the audio event is activated
            if self.send_audio_event.is_set():
                try:
                    self.aud_socket.sendall(data)
                except Exception as e:
                    print("Audio send error:", e)
                    break
        
    # Handles when user sends message of their input
    def sendMessage(self, message):
        if not message:
            return

        try:
            self.client_socket.sendall(message.encode("utf-8"))
        except Exception as e:
            print(f"Error found while sending the message: {e}")
           
    # Activate the trucking options which deactivates the tracking if it's on
    def set_trucking(self, option):
        if option == "Forward":
            self.toggleForwardTrucking()
            if self.forwardTrucking:
                print("Activate forward trucking")
                self.forward_trucking.configure(fg_color="green")
                self.backward_trucking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
            else:
                print("Deactivate forward trucking")
                self.forward_trucking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
                
        elif option == "Back":
            self.toggleBackwardTrucking()
            if self.backwardTrucking:
                print("Activate backward trucking")
                self.backward_trucking.configure(fg_color="green")
                self.forward_trucking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
            else:
                print("Deactivate backward trucking")
                self.backward_trucking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
        
    # Activate the tracking options which deactivates the trucking if it's on
    def set_tracking(self, option):
        if option == "Sideways":
            self.toggleSidewayTracking()
            if self.tracking:
                print("Activate sideway tracking")
                self.sideway_tracking.configure(fg_color="green")
                self.rotate_tracking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
            else:
                print("Deactivate sideway tracking")
                self.sideway_tracking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
                
        if option == "Rotate":
            self.toggleRotateTrack()
            if self.rotate_track:
                print("Activate sideway tracking")
                self.sideway_tracking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
                self.rotate_tracking.configure(fg_color="green")
            else:
                print("Deactivate rotate tracking")
                self.rotate_tracking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
            
    # Toggle the tracking options, closes the trucking and update the states
    def toggleTrackingOptions(self):
        if not self.showTrackingOptions:
            self.tracking = False
            self.forwardTrucking = False
            self.backwardTrucking = False
            # self.manualMove = False
            self.rotate_track = False
            
            self.sideway_tracking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
            self.rotate_tracking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
        else:
            self.showTruckingOptions = False
            self.backward_trucking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
            self.forward_trucking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
            
    # Toggle the trucking options, closes the tracking and update the states
    def toggleTruckingOptions(self):
        if not self.showTruckingOptions:
            self.forwardTrucking = False
            self.backwardTrucking = False
            
            self.backward_trucking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
            self.forward_trucking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
        else:
            self.showTrackingOptions = False
            self.sideway_tracking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
            self.rotate_tracking.configure(fg_color=("#3B8ED0", "#1F6AA5"))
        
    # Toggle the forward trucking from the trucking options
    def toggleForwardTrucking(self):
        if not self.forwardTrucking:
            self.tracking = False
            self.forwardTrucking = True
            self.backwardTrucking = False
            self.rotate_track = False
        else:
            self.forwardTrucking = False
            
    # Toggle the backward trucking from the trucking options
    def toggleBackwardTrucking(self):
        if not self.backwardTrucking:
            self.tracking = False
            self.forwardTrucking = False
            self.backwardTrucking = True
            self.rotate_track = False
        else:
            self.backwardTrucking = False
            
    # toggle the sideway track button from the tracking options
    def toggleSidewayTracking(self):
        if not self.tracking:
            self.tracking = True
            self.forwardTrucking = False
            self.backwardTrucking = False
            self.rotate_track = False
        else:
            self.tracking = False
            
    # toggle the rotate track button from the tracking options
    def toggleRotateTrack(self):
        if not self.rotate_track:
            self.tracking = False
            self.forwardTrucking = False
            self.backwardTrucking = False
            self.rotate_track = True
        else:
            self.rotate_track = False
            
    def updateLeftbutton(self, button, idx):
        if idx in [2, 3]:
            for i, btn in enumerate(self.left_buttons):
                if i in [2, 3]:
                    if btn != button:
                        btn.configure(fg_color=("#3B8ED0", "#1F6AA5"))
                        
    def updateRightbutton(self, button, idx):
        if idx in [3, 4]:
            for i, btn in enumerate(self.right_buttons):
                if i in [3, 4]:
                    if btn != button:
                        btn.configure(fg_color=("#3B8ED0", "#1F6AA5"))
        
# Starting the client
def start_client():
    try:
        # Create BOTH sockets first
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # client socket for streaming, robot and camera controls
        aud_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Audio socket for smooth audio transfer

        # Connect command FIRST (important for responsiveness)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to command server")

        # Then connect audio
        aud_sock.connect((SERVER_HOST, AUD_PORT))
        print("Connected to audio server")

        # Start GUI
        app = MovieDirectorGUI(client_socket, aud_sock)
        app.mainloop()

    except ConnectionRefusedError:
        print(f"Connection to server failed. Is it running?")

    except Exception as e:
        print(f"Error from starting the client: {e}")

    finally:
        # Clean shutdown
        try:
            client_socket.close()
        except Exception as e:
            print(f"Error found while closing the client socket: {e}")

        try:
            aud_sock.close()
        except Exception as e:
            print(f"Error found while closing the audio socket: {e}")

if __name__ == "__main__":
    start_client()