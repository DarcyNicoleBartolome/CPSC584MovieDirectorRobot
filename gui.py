import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import threading
import time
import os

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
# for visualizing results
# from mediapipe.framework.formats import landmark_pb2

# Test hollistic tracking
# import mediapipe as mp
import numpy as np
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
        connection_drawing_spec=pose_connection_style)

  return annotated_image

CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"

# !! Change into the Robot's IP when testing with the group5 SD card
SERVER_HOST = "172.17.10.218" # Raspy's with CPSC584 wifi
# SERVER_HOST = "10.0.0.116" # localhost
SERVER_PORT = 5001


# !! TODO LOOK AT CHUNKS IN AUDIO AND SUCH!!!!


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# def mediapipe_test(cap):
#     # print(f"Starting stream with: {capture}")
   
#     pTime = 0
#     cTime = 0

#    # access webcam
#     # cap = cv2.VideoCapture(capture, cv2.CAP_FFMPEG)
#     # # cap = cv2.VideoCapture(capture)
#     # cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
#     print(cap)
    
#     while True:
#         ret, img = cap.read()
#         if not ret or img is None:
#             print("Failed to grab frame")
#             continue

#         frame = img.copy()
        
#         if frame is not None:
#             try:
#                 cv2.imshow("frame", frame)
#             except Exception as e:
#                 print("imshow crash:", e)

        # if cv2.waitKey(0) == ord('q'):
        #     break

    # while True:
    #     # pull frame
    #     ret, frame = cap.read()
    #     #   frame = capture
    #     if not ret:
    #         print("Failed to grab frame")
    #         break

    #     image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     image.flags.writeable = False

    #   # display image
    #     print("Showing image")
    #     cv2.imshow('frame', frame)
    #     if cv2.waitKey(25) == ord('q'):
    #         break   
   
    # cap.release()
    # cv2.destroyAllWindows()
    
    
    
    
    
# class landmarker_and_result():
#     def __init__(self):
#             self.result = None
#             self.image_for_drawing = None
#             self.lock = False  # Prevent multiple updates at once
#             self.landmarker = mp.tasks.vision.HandLandmarker
#             self.createLandmarker()
    
#     def createLandmarker(self):
#         # callback function
#             def update_result(result: mp.tasks.vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
#                 if not self.lock:
#                     self.lock = True
#                     self.result = result
#                     self.image_for_drawing = output_image.numpy_view()  # Save output image
#                     self.lock = False

#             # HandLandmarkerOptions (details here: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker/python#live-stream)
#             options = mp.tasks.vision.HandLandmarkerOptions( 
#                 base_options = mp.tasks.BaseOptions(model_asset_path="/hand_landmarker.task"),
#                 running_mode = mp.tasks.vision.RunningMode.LIVE_STREAM, # running on a live stream
#                 num_hands = 4, # track one hand/s
#                 min_hand_detection_confidence = 0.3, # lower than value to get predictions more often
#                 min_hand_presence_confidence = 0.3, # lower than value to get predictions more often
#                 min_tracking_confidence = 0.3, # lower than value to get predictions more often
#                 result_callback=update_result)
        
#             # initialize landmarker
#             self.landmarker = self.landmarker.create_from_options(options)
    
#     def detect_async(self, frame):
#         # convert np frame to mp image
#         mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
#         # detect landmarks
#         self.landmarker.detect_async(image = mp_image, timestamp_ms = int(time.time() * 1000))

    # def close(self):
    #     # close landmarker
    #     self.landmarker.close()





# def draw_landmarks_on_image(rgb_image, detection_result: mp.tasks.vision.HandLandmarkerResult):
#    """Courtesy of https://github.com/googlesamples/mediapipe/blob/main/examples/hand_landmarker/python/hand_landmarker.ipynb"""
#    try:
#       if detection_result.hand_landmarks == []:
#          return rgb_image
#       else:
#          hand_landmarks_list = detection_result.hand_landmarks
#          handedness_list = detection_result.handedness
#          annotated_image = np.copy(rgb_image)

#          # Loop through the detected hands to visualize.
#          for idx in range(len(hand_landmarks_list)):
#             hand_landmarks = hand_landmarks_list[idx]
            
#             # Draw the hand landmarks.
#             hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
#             hand_landmarks_proto.landmark.extend([
#                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks])
#             mp.solutions.drawing_utils.draw_landmarks(
#                annotated_image,
#                hand_landmarks_proto,
#                mp.solutions.hands.HAND_CONNECTIONS,
#                mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
#                mp.solutions.drawing_styles.get_default_hand_connections_style())

#          return annotated_image
#    except:
#       return rgb_image

# def count_fingers_raised(rgb_image, detection_result: mp.tasks.vision.HandLandmarkerResult):
#     """Iterate through each hand, checking if fingers (and thumb) are raised.
#     Hand landmark enumeration (and weird naming convention) comes from
#     https://developers.google.com/mediapipe/solutions/vision/hand_landmarker."""
#     try:
#         # Get Data
#         hand_landmarks_list = detection_result.hand_landmarks
#         # Counter
#         numRaised = 0
#         # for each hand...
#         for idx in range(len(hand_landmarks_list)):
#             # hand landmarks is a list of landmarks where each entry in the list has an x, y, and z in normalized image coordinates
#             hand_landmarks = hand_landmarks_list[idx]
#             # for each fingertip... (hand_landmarks 4, 8, 12, and 16)
#             for i in range(8,21,4):
#                 # make sure finger is higher in image the 3 proceeding values (2 finger segments and knuckle)
#                 tip_y = hand_landmarks[i].y
#                 dip_y = hand_landmarks[i-1].y
#                 pip_y = hand_landmarks[i-2].y
#                 mcp_y = hand_landmarks[i-3].y
#                 if tip_y < min(dip_y,pip_y,mcp_y):
#                     numRaised += 1
#             # for the thumb
#             # use direction vector from wrist to base of thumb to determine "raised"
#             tip_x = hand_landmarks[4].x
#             dip_x = hand_landmarks[3].x
#             pip_x = hand_landmarks[2].x
#             mcp_x = hand_landmarks[1].x
#             palm_x = hand_landmarks[0].x
#             if mcp_x > palm_x:
#                 if tip_x > max(dip_x,pip_x,mcp_x):
#                     numRaised += 1
#             else:
#                 if tip_x < min(dip_x,pip_x,mcp_x):
#                     numRaised += 1
            
            
#         # display number of fingers raised on the image
#         annotated_image = np.copy(rgb_image)
#         height, width, _ = annotated_image.shape
#         text_x = int(hand_landmarks[0].x * width) - 100
#         text_y = int(hand_landmarks[0].y * height) + 50
#         cv2.putText(img = annotated_image, text = str(numRaised) + " Fingers Raised",
#                             org = (text_x, text_y), fontFace = cv2.FONT_HERSHEY_DUPLEX,
#                             fontScale = 1, color = (0,0,255), thickness = 2, lineType = cv2.LINE_4)
#         return annotated_image
#     except:
#         return rgb_image


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
        self.stream_url = "http://172.17.10.218:8080/stream.mjpg"
        # self.stream_url = "http://10.0.0.116:8080/stream.mjpg"
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # # For audio streaming
        # # Test Director Speaker
        self.setSpeaker = False
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
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
        
        # Display Zoom state
        self.showZoom = False
        self.current_zoomvalue = 1
        
        
        # Left side icons: camera, focus, zoom
        left_icons = ["icons/camera.png", "icons/focus2.png", "icons/zoom.png", "icons/autofocus.png", "icons/colorFilter.png", "icons/joystick.png", "icons/lock.png"]
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
        
        self.left_photos = left_photos  # Keep references

        # Right
        self.right = ctk.CTkFrame(self, corner_radius=16)
        self.right.grid(row=0, column=2, padx=(10, 18), pady=(18, 10), sticky="ns")
        
        # Right side icons: goldenratio, and others to be added
        right_icons = ["icons/goldenratio2.png", "icons/icon2.png", "icons/icon3.png", "icons/rule-of-thirds.png", "icons/center.png"]
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

        # Bottom bar
        self.bottom = ctk.CTkFrame(self, corner_radius=16)
        self.bottom.grid(row=1, column=0, columnspan=3, padx=18, pady=(10, 18), sticky="ew")
        
        # !! TEST SLIDER design
        
        self.zoom_slider = ctk.CTkSlider(
                self.center,
                from_=1, 
                to=8,
                # fg_color=,
                number_of_steps=100,
                command=lambda value=i: self.zoom_value(value)
            )
        self.zoom_slider.set(self.current_zoomvalue)
        
        self.AF_slider = ctk.CTkSlider(
                self.center,
                from_=0,
                # from_=0.55, to=2.75, digits = 3, resolution = 0.01  #!! Find a way to may it float
                to=10,
                # fg_color=,
                # number_of_steps=10,
                command=lambda value=i: self.AfManual(value)
            )
        self.AF_slider.set(0)
        
        # Add color filters
        self.colorFilterControls = ctk.CTkFrame(self.center, corner_radius=16)
        
        self.colorFilterControls.place(relx=250, rely=20)
        text_filters = ["RGGB", "GRBG", "GBRG", "BGGR", "B/W"]
        ctk.CTkButton(
                    self.colorFilterControls, 
                    text="RGGB",
                    width=52, 
                    height=52, 
                    corner_radius=14,
                    command=lambda idx=i: self.on_right_action(idx),
                ).place(relx=2, rely=2)
        # for i, text in text_filters:
        

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
            print(f"Error loading {icon}: {e}")
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
            print(f"Error loading {icon}: {e}")
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
            print(f"Error loading record image: {e}")
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
            print(f"Error loading pause image: {e}")
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

        # Record button (red) with image
        try:
            record_path = os.path.join(project_dir, "icons/record.png")
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
            pause_path = os.path.join(project_dir, "icons/pause.png")
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
            stop_path = os.path.join(project_dir, "icons/stop.png")
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
        self.utility.grid(row=0, column=3, padx=12, pady=12, sticky="e")

        # Gallery button with image
        try:
            gallery_path = os.path.join(project_dir, "icons/gallery.png")
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
            speaker_path = os.path.join(project_dir, "icons/speaker.png")
            speaker_img = Image.open(speaker_path)
            speaker_img = speaker_img.resize((40, 40), Image.Resampling.LANCZOS)
            speaker_photo = ImageTk.PhotoImage(speaker_img)
            self.speaker_photo = speaker_photo  # Keep a reference
            
            speaker = ctk.CTkButton(
                self.utility,
                image=speaker_photo,
                text="",
                width=45,
                height=45,
                corner_radius=14,
                command=lambda: self.directorSpeaker()
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
            )
            speaker.pack(side="left", padx=6)

        # Settings button with image
        try:
            settings_path = os.path.join(project_dir, "icons/settings.png")
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
            # Test mediapipe 
            # threading.Thread(target=mediapipe_test, args=(self.cap,), daemon=True).start()
        
        # Initialize PoseLandmarker once
        base_options = python.BaseOptions(model_asset_path='pose_landmarker_full.task')
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=False)
        self.pose_detector = vision.PoseLandmarker.create_from_options(options)
            
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(33, self._render_latest_frame)
        
        # --- Director Speaker stream state --- 
        self.send_audio_event = threading.Event()
        # self.send_audio_event.set()  # audio enabled
        threading.Thread(target=self.audio_sender, daemon=True).start()
        
        
        
        # !! ROBOT SPEED CHANGE POSITION LATER
        self.speed_label = ctk.CTkLabel(
                self.utility,
                text=str(self.speed),
                font=("Arial", 32)
            )
        self.speed_label.pack(side="left", padx=6) 

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
            
            # mirror frame
            # frame = cv2.flip(frame, 1)
            # resized_frame = cv2.resize(frame, (320, 240))

            # BGR -> RGB
            self._latest_frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def _render_latest_frame(self):
        image = self._latest_frame_rgb
        
        if image is not None:
            w = self.preview.winfo_width()
            h = self.preview.winfo_height()
            if w > 10 and h > 10:
                image = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)

            # Convert numpy array to MediaPipe Image format
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

            # Detect pose landmarks from the input image
            detection_result = self.pose_detector.detect(mp_image)
            # result = detection_result.pose_landmarks
            # print(result)
            # print(len(result))
            
            self.process_result(detection_result, w, h)
            
            # print(w, h)

            # Process the detection result and draw landmarks
            annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), detection_result)
            
            # cv2.circle(annotated_image, (w, h), 75, (255, 0, 0), 10)
            # cv2.circle(annotated_image, (int(w/2), int(h/2)), 25, (255, 0, 0), 10)
            
            # 5 lines
            cv2.line(annotated_image, (int(w/5), 0), (int(w/5), h), (0, 255, 0), 3)
            cv2.line(annotated_image, (int(w/5)*2, 0), (int(w/5)*2, h), (0, 255, 0), 3)
            cv2.line(annotated_image, (int(w/5)*3, 0), (int(w/5)*3, h), (0, 255, 0), 3)
            cv2.line(annotated_image, (int(w/5)*4, 0), (int(w/5)*4, h), (0, 255, 0), 3)
            
            # # Rule of thirds line
            # cv2.line(annotated_image, (int(w/3), 0), (int(w/3), h), (0, 255, 0), 3)
            # cv2.line(annotated_image, (int(w/3)*2, 0), (int(w/3)*2, h), (0, 255, 0), 3)
            # cv2.line(annotated_image, (0, int(h/3)), (w, int(h/3)), (0, 255, 0), 3)
            # cv2.line(annotated_image, (0, int(h/3)*2), (w, int(h/3)*2), (0, 255, 0), 3)
            


            # Convert to PhotoImage for Tkinter display
            annotated_image_pil = Image.fromarray(annotated_image)
            annotated_imgtk = ImageTk.PhotoImage(annotated_image_pil)
            
            
            
            self.video_label.configure(image=annotated_imgtk)
            # self.video_label.image = annotated_imgtk  # Keep a reference

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
        
        if idx == 2: # Zoom button is clicked
            self.showZoom = not self.showZoom
            if self.showZoom:
                # self.zoom_slider.grid(row=1, column=0, columnspan=3, padx=18, pady=(10, 18), sticky="ew")
                self.zoom_slider.place(relx=0.5, rely=0.9, relwidth=0.7, relheight=0.06, anchor='center')
                print("open zoom slider")
            else:
                print("close zoom slider")
                # self.zoom_slider.configure(state="disabled")
                self.zoom_slider.place_forget()
            
                
        if idx == 3: # If Autofocus is clicked
            # Right now test the manual len position
            self.setAfManual = not self.setAfManual
            if self.setAfManual:
                print("open autofocus slider")
                self.AF_slider.place(relx=0.5, rely=0.9, relwidth=0.7, relheight=0.06, anchor='center')
            else:
                print("close autofocus slider")
                # self.zoom_slider.configure(state="disabled")
                self.AF_slider.place_forget()
            
    def AfManual(self, value):
        time.sleep(0.05)
        print("Lens position: ", value)
        # state = "+"
        # if value < self.current_zoomvalue:
        #     state = "-"
        # self.current_zoomvalue = value
        self.sendMessage(f"autofocus:{value}")
        
    def process_result(self, detection_result, w, h):
        get_body = detection_result.pose_landmarks
        list = []
        if len(get_body) == 0:
            return
        result = get_body[0]
        right_sx = float(result[12].x * w)
        list.append(right_sx)
        # right_sy = float(result[12].y * h)
        
        left_sx = float(result[11].x * w)
        list.append(left_sx)
        # left_sy = float(result[11].y - (h/2))
        
        right_hx = float(result[24].x * w)
        list.append(right_hx)
        # right_hy = float(result[24].y - (h))
        
        left_hx = float(result[23].x * w)
        list.append(left_hx)
        # left_hy = float(result[23].y - (h))
        
        # Convert to percentage offset
        # right_sx /= float(w/2)
        # right_sy /= float(h/2)
        
        # left_sx /= float(w/2)
        # left_sy /= float(h/2)
        
        # right_hx /= float(w)
        # right_hy /= float(h)
        
        # left_hx /= float(w)
        # left_hy /= float(h)
        
        # print(right_sx)
        # print(right_sy)
        # print(left_sx)
        # print(left_sy)
        # print(right_hx)
        # print(right_hy)
        # print(left_hx)
        # print(left_hy)
        
        # Source - https://stackoverflow.com/a/10285205
# Posted by ninjagecko, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-30, License - CC BY-SA 4.0

        # !! if tracking is on TRACKING
        # Move left if atleast 2 points of the torso is at w/5 at the left of the screen
        if sum(2 for x in list if x < w/5) >= 2:
            self.sendMessage(f"move:left")
        
        # Move right if atleast 2 points of the torso is at w/5 at the right of the screen
        if sum(2 for x in list if x > w/5*4) >= 2:
            self.sendMessage(f"move:right")

        # !! TRUCKING
        # Move forward if shoulders are too far
        # if (abs(left_sx-right_sx) < 80):
        #     self.sendMessage(f"move:up")
        
        # !! RULE OF THIRDS
        # print(abs(left_sx-right_sx))
        
        # !! SYMMETRY
        # if (right_sx > int(w/5)*2
        #     and (left_sx < int(w/5)*3)):

        
        ## !! NONE FOR NOW
        # if (right_sx < 0.1 or right_sy < 0.1 or left_sx < 0.1 or left_sy < 0.1 or right_hx < 0.1 or right_hy < 0.1 or 
        #     left_hx < 0.1 or left_hy < 0.1):
            
        #     self.sendMessage(f"move:right")
            
        # elif (right_sx < 0.9 or right_sy < 0.9 or left_sx < 0.9 or left_sy < 0.9 or right_hx < 0.9 or right_hy < 0.9 or 
        #     left_hx < 0.9 or left_hy < 0.9):
            
        #     self.sendMessage(f"move:left")

        

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
        
        if (direction == "+"):
            self.speed += 5
            self.speed_label.configure(text=str(self.speed))
        elif (direction == "-"):
            self.speed -= 5
            self.speed_label.configure(text=str(self.speed))
        
    def directorSpeaker(self):
        self.setSpeaker = not self.setSpeaker
        print(f"set speaker: {self.setSpeaker}") 
        
        if self.send_audio_event.is_set():
            self.send_audio_event.clear()
        else:
            self.send_audio_event.set()
        
    # def audio_sender(self):
    #     print("Audio thread started")
    #     while True:
    #         if self.send_audio_event.is_set():
    #             data = self.stream.read(CHUNK, exception_on_overflow=False)
    #             self.client_socket.sendall(data)
    #         else:
    #             time.sleep(0.01) 
    
    def audio_sender(self):
        print("Audio thread started")

        while True:
            data = self.stream.read(CHUNK-4, exception_on_overflow=False) # Attempt removing 4 bytes for AUD:

            if self.send_audio_event.is_set():
                try:
                    # self.client_socket.sendall(b"AUD:" + data)
                    self.client_socket.sendall(data)
                except Exception as e:
                    print("Audio send error:", e)
                    break
        
    # Handles when user sends message of their input
    def sendMessage(self, message):
        # If user tries to send an empty message, nothing happens and return
        if not message:
            return
        
        try:
            # if the client did not send a command, send it to the server as a message the user want to broadcast to all users in the chatroom
            self.client_socket.sendall(message.encode("utf-8"))
            
        except Exception as e: # If other Exception error detected, print out the error and close the chatroom window after half a second
            print(f"Error found while sending the message: {e}")
        
def start_client():
    """ Start the client and connect to the server. """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            # Setting up the GUI
            app = MovieDirectorGUI(client_socket)
            # Starts the Tkinter event loop to run and show the GUI
            app.mainloop()
    
    except ConnectionRefusedError: # If connection error detected, print out the error
        print(f"Connection to {SERVER_HOST}:{SERVER_PORT} failed. Ensure the server is running.")
    
    except Exception as e: # If other Exception error detected, print out the error
        print(f"An error occurred while running the application: {e}")
        print(f"You are forced to leave the chatroom... Please retry and come back again")

if __name__ == "__main__":
    start_client()
    # app = MovieDirectorGUI()
    # app.mainloop()