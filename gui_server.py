
import threading
import os

from picrawler import Picrawler
from time import sleep
import readchar
from libcamera import controls
# Attempt socket programming
import socket
import pyaudio

# import for video streaming
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput

from http.server import BaseHTTPRequestHandler, HTTPServer
import io

import subprocess

HOST = "172.17.10.222" # Raspy's with CPSC584 wifi
PORT = 5001
AUD_PORT = 5002

crawler = Picrawler()
speed = 90

leg_mode = 0

LENGTH_SIDE = 77
X_DEFAULT = 45
X_TURN = 70
# X_START = 0
X_START = 10 # Widen abit
Y_DEFAULT = 45
Y_TURN = 130
Y_WAVE =120
Y_START = 10 # widen abit to avoid covering the screen 
# Y_START = 0 
Z_DEFAULT = -50
Z_UP = -30
Z_WAVE = 60
Z_TURN = -40
Z_PUSH = -76

# Audio

p = pyaudio.PyAudio()
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)


# Initialize picamera
picam2 = Picamera2()
size = None
full_res = None

#region ######### Video streaming #########
class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = threading.Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

output = StreamingOutput()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/stream.mjpg", "/"):
            self.send_error(404)
            return

        # simple landing page
        if self.path == "/":
            page = b"<html><body><img src='/stream.mjpg'></body></html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)
            return

        # MJPEG stream endpoint
        self.send_response(200)
        self.send_header("Age", "0")
        self.send_header("Cache-Control", "no-cache, private")
        self.send_header("Pragma", "no-cache")
        self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=FRAME")
        self.end_headers()

        try:
            while True:
                with output.condition:
                    output.condition.wait()
                    frame = output.frame

                self.wfile.write(b"--FRAME\r\n")
                self.send_header("Content-Type", "image/jpeg")
                self.send_header("Content-Length", str(len(frame)))
                self.end_headers()
                self.wfile.write(frame)
                self.wfile.write(b"\r\n")
        except Exception:
            pass
   
         
def zoom(value, state):
   global picam2
   global size
   global full_res

   # sync up the arrival of the new frame
   picam2.capture_metadata()

   zoom = float(value)

   sensor_w, sensor_h = full_res

   # calculate crop size
   crop_w = int(sensor_w / zoom)
   crop_h = int(sensor_h / zoom)

   # center crop
   offset_x = (sensor_w - crop_w) // 2
   offset_y = (sensor_h - crop_h) // 2

   picam2.set_controls({
      "ScalerCrop": [offset_x, offset_y, crop_w, crop_h]
   })
   

def VideoStream():
   global picam2
   global size
   global full_res
   
   # You can change size/fps later
   picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
   picam2.start_recording(MJPEGEncoder(), FileOutput(output))
   
   # Set the size and full resolution (vital for the zoom function)
   size = picam2.capture_metadata()['ScalerCrop'][2:]
   full_res = picam2.camera_properties['PixelArraySize']

   server = HTTPServer(("0.0.0.0", 8080), Handler)
   print("MJPEG stream:")
   print("  http://<PI_IP>:8080/stream.mjpg")
   print("  http://<PI_IP>:8080/  (preview page)")
   server.serve_forever()
    
#endregion ######### Video streaming #########

#region ######### Crawler Movement #########

# Robot move to the left side
def move_sideLeft(speed, current, amount=2.5):
   global leg_mode
   crawler.stand_position = crawler.stand_position + 1 & 1
   step_amount = amount
   
   # List of the step of moving to the left, starting with the left backleg
   left_backleg_move =  [
      ## [right front],[left front],[left rear],[right rear]
      
      # Lifts the left rear leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_START, X_TURN, Z_UP],[Y_START, X_DEFAULT, Z_DEFAULT]], 
      
      # move the left rear leg to the left
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*step_amount, X_DEFAULT, Z_UP],[Y_START, X_DEFAULT, Z_DEFAULT]],
      
      # Put down the left rear leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*step_amount, X_DEFAULT,Z_DEFAULT],[Y_START, X_DEFAULT, Z_DEFAULT]],
      
      # Move the rest legs to the leg
      [[Y_DEFAULT*step_amount, X_DEFAULT, Z_DEFAULT],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      # [[Y_DEFAULT-30, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_START, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Lift the right front leg up
      [[Y_DEFAULT*step_amount, X_DEFAULT, Z_UP],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT]],
      # [[Y_DEFAULT-30, X_DEFAULT, Z_UP],[Y_DEFAULT, X_START, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT]],
      
      # Move the right front leg to the left
      [[X_START, Y_DEFAULT, Z_UP],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # # Put down the right front rear leg
      [[X_START, X_TURN, Z_DEFAULT],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
   ]
   
   # List of the step of moving to the left, starting with the left frontleg
   left_frontleg_move =  [
      
      # Lifts the left front leg
      [[X_START, X_TURN, Z_DEFAULT],[Y_START, X_TURN, Z_UP],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # move the left front leg to the left
      [[X_START, X_TURN, Z_DEFAULT],[Y_DEFAULT*step_amount, X_DEFAULT, Z_UP],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Put down the left front leg
      [[X_START, X_TURN, Z_DEFAULT],[Y_DEFAULT*step_amount, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Move the rest legs to the leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT*step_amount, X_DEFAULT, Z_DEFAULT]],
      
      # Lift the right back leg up
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_START, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*step_amount, X_DEFAULT, Z_UP]],
      
      # Move the right back leg to the left
      [[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_START, X_DEFAULT, Z_DEFAULT],[X_START, Y_DEFAULT, Z_UP]],
      
      # # Put down the right back leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[X_START, X_DEFAULT, Z_DEFAULT],[Y_START, X_DEFAULT, Z_DEFAULT]], 
   ]
   
   # Determine which front or back leg should move
   if leg_mode == 0:
      for coord in left_backleg_move:
         crawler.do_step(coord, speed)
         # sleep(1)
         print(coord)
      leg_mode = 1
   else:     
      for coord in left_frontleg_move:
         crawler.do_step(coord, speed)
         # sleep(1)
         print(coord)
      leg_mode = 0
   
   
# Robot move to the right side
def move_sideRight(speed, current, amount=2.5):
   global leg_mode
   
   crawler.stand_position = crawler.stand_position + 1 & 1
   
   step_amount = amount
   
   # List of the step of moving to the right, starting with the right backleg
   right_backleg_move =  [
      
      # Lifts the right rear leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_START, X_DEFAULT, Z_DEFAULT],[Y_START, X_TURN, Z_UP]], 
      
      # move the right rear leg to the left
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_START, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*step_amount, X_DEFAULT, Z_UP]],
      
      # Put down the right rear leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_START, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*step_amount, X_DEFAULT, Z_DEFAULT]],
      
      # Move the rest legs to the leg
      [[X_START, Y_DEFAULT, Z_DEFAULT], [Y_DEFAULT*step_amount, X_DEFAULT, Z_DEFAULT], [Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Lift the left front leg up
      [[X_START, Y_DEFAULT, Z_DEFAULT], [Y_DEFAULT*step_amount, X_DEFAULT, Z_UP], [Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT]],
      
      # Move the left front leg to the left
      [[X_START, Y_DEFAULT, Z_DEFAULT], [X_START, Y_DEFAULT, Z_UP], [Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # # Put down the left front rear leg
      [[X_START, Y_DEFAULT, Z_DEFAULT], [X_START, X_TURN, Z_DEFAULT], [Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
   ]
   
   # List of the step of moving to the right, starting with the right frontleg
   right_frontleg_move =  [
      
      # Lifts the right front leg
      [[Y_START, X_TURN, Z_UP], [X_START, X_TURN, Z_DEFAULT], [Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # move the right front leg to the left
      [[Y_DEFAULT*step_amount, X_DEFAULT, Z_UP], [X_START, X_TURN, Z_DEFAULT], [Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Put down the right front leg
      [[Y_DEFAULT*step_amount, X_DEFAULT, Z_DEFAULT], [X_START, X_TURN, Z_DEFAULT], [Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Move the rest legs to the leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*step_amount, X_DEFAULT, Z_DEFAULT], [X_START, Y_DEFAULT, Z_DEFAULT]],
      
      # Lift the left back leg up
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*step_amount, X_DEFAULT, Z_UP],[X_START, X_DEFAULT, Z_DEFAULT]],
      
      # Move the left back leg to the left
      [[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_START, Y_DEFAULT, Z_UP],[X_START, X_DEFAULT, Z_DEFAULT]],
      
      # # Put down the left back leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[Y_START, X_DEFAULT, Z_DEFAULT],[X_START, X_DEFAULT, Z_DEFAULT]], 
   ]
   
   # Determine which front or back right should move
   if leg_mode == 0:
      for coord in right_backleg_move:
         crawler.do_step(coord, speed)
         print(coord)
      leg_mode = 1
   else:     
      for coord in right_frontleg_move:
         crawler.do_step(coord, speed)
         print(coord)
      leg_mode = 0

# Robot rotate left
def move_rotateLeft(speed, current_pose):
   crawler.do_action('turn left', 1, speed)
# Robot rotate right
def move_rotateRight(speed, current_pose):
   crawler.do_action('turn right', 1, speed)
# Robot move forward
def moveUp(speed, current):
   crawler.do_action('forward', 1, speed)
# Robot move backward
def moveDown(speed, current):
   crawler.do_action('backward', 1, speed)
# Robot look up
def lookUp(speed, current):
   coords = [
      [[45, 45, -76], [45, 0, -76], [45, 0, -38], [45, 45, -30]],
   ]
   # Play all the steps
   for coord in coords:
      crawler.do_step(coord, speed)

# Robot look down
def lookDown(speed, current):
    coords = [
        # stand
        [[45, 45, -28], [45, 0, -40], [45, 0, -68], [45, 45, -76]],
    ]
    # Play all the steps
    for coord in coords:
        crawler.do_step(coord, speed)
        
# Robot plays the audio received from the client, only happens when directors speaker is on
def handle_audio(conn):
    while True:
        data = conn.recv(4096)
        if not data:
            break
        print("Audio chunk:", len(data))
        stream.write(data)
        
#endregion ######### Crawler Movement #########

#region ######### Socket Programming / Start running the server #########
   
def start_server():
   """ Start the server and listen for incoming connections. """
   # Audio socket
   aud_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   aud_sock.bind((HOST, AUD_PORT))
   aud_sock.listen(1)
   
   server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server_socket.bind((HOST, PORT))
   server_socket.listen(5)
   print(f"Server started and listening on {HOST}:{PORT}")
      
   threading.Thread(target=VideoStream).start()
      
   while True:
         try:
            # Accept new client connections and start a thread for each client
            client_socket, client_address = server_socket.accept()
            aud_conn, _ = aud_sock.accept()
            
            # If connections are successful, create threads for handling robot and aud data
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
            threading.Thread(target=handle_audio, args=(aud_conn,), daemon=True).start()
         except Exception as e:
            print(f"Error accepting connections: {e}")
            
         except KeyboardInterrupt:
            print("\nShutting down server...")

         finally:
            print("Closing sockets...")
            server_socket.close()
            aud_sock.close()
            
         current_pose = crawler.current_step_all_leg_value()
         crawler.do_step(current_pose, speed) # Attempt not avoid the robot to stay relaxed
               

# Handle incoming client data
def handle_client(client_socket, client_address):
   """ Handle incoming client requests. """
   print(f"Connection from {client_address}")
   global speed 
   speed = 90 # Reset speed to 90
   setup = [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT]]
   crawler.do_step(setup, speed)
   
   try:
      while True:
         # Receive data from the client
         request_data = client_socket.recv(CHUNK)
         if not request_data:  # Client has closed the connection
            break
         # Print the received request from the client
         print(f"Received request: {request_data} from {client_address}")
         
         # Here, the request is processed to determine the response
         process_request(request_data, client_socket, client_address)
            
   except Exception as e:
         # print the error found while reading the client's data
         print(f"Error Found in Client's data: {e}")
         
   finally:
         # Close the client connection with grace
         client_socket.close()
         # print that the client has close connection with the server and store to a server log
         print(f"Closed connection with {client_address}")         
            
def process_request(data, client_socket, client_address):
   """ Process the client's request and generate a response. """
   global speed
   current_pose = crawler.current_step_all_leg_value()
   # Decode the request data
   request_data = data.decode("utf-8", errors="replace")
   if not request_data or request_data == "":
      client_socket.sendall("".encode("utf-8"))
      print(f"the request data is empty")
      return
   
   # Add \n at the end
   """Some data will have multiple \n to process all data in that one line, while other data only need one for real-time accuracy"""
   if "\n" not in request_data:
      request_data = request_data + "\n"
   
   # Process all the data by each \n in the line
   while "\n" in request_data:
      message, request_data = request_data.split("\n", 1)
      print("process request", message)
      
      if not message:
         continue
   
      # parse the message
      message = message.split(':')

      # If header has move, robot will react based on the direction command
      if message[0] == "move":
         # print("Move activated") # Debug print
         if 'left' == message[1]: # move sideway left
            move_sideLeft(speed, current_pose)
         elif 'rotate left' == message[1]: # rotate left
            move_rotateLeft(speed, current_pose)
         elif 'rotate right' == message[1]: # rotate right
            move_rotateRight(speed, current_pose)
         elif 'right' == message[1]: # move sideway right
            move_sideRight(speed, current_pose)
         elif 'look up' == message[1]: # look up
            lookUp(speed, current_pose)
         elif 'look down' == message[1]: # look down
            lookDown(speed, current_pose)
         elif 'up' == message[1]: # move forward
            moveUp(speed, current_pose)
         elif 'down' == message[1]: # move backward
            moveDown(speed, current_pose)
         elif 'stand' == message[1]: # move to a stand position
            crawler.do_step('stand', speed)
         elif '+' == message[1]: # increase robot speed by 5
            speed+=5
            print(speed)
         elif '-' == message[1]: # decrease robot speed by 5
            speed-=5
            print(speed)
         else: return # Do nothing
         
      elif message[0] == "zoom": # Set the function of the camera based on the value
         # print("Zoom On") # Debug print
         zoom(message[1], message[2])
   

# If runs, the server starts
if __name__ == '__main__':
    start_server()
    
# after main close stop all audio processes
stream.stop_stream()
stream.close()
p.terminate()