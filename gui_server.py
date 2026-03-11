
import threading
# import time
import os

from picrawler import Picrawler
from time import sleep
import readchar

# Attempt socket programming
import socket
import pyaudio

import subprocess

# !! Change into the Robot's IP when testing with the group5 SD card
HOST = "172.17.10.158" # Raspy's with CPSC584 wifi
PORT = 5001

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

# p = pyaudio.PyAudio()
# CHUNK = 1024 * 4
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100

# stream = p.open(format=FORMAT,
#                 channels=CHANNELS,
#                 rate=RATE,
#                 output=True,
#                 frames_per_buffer=CHUNK)

def stand(speed, current): # make the robot stand up
   test = [i for i in current]
   i = 0 # counter
   for leg in test:
      if leg[2] != Z_DEFAULT:
          test[i][2] = Z_DEFAULT
          i += 1

   crawler.do_step(test, speed)

def move_sideLeft(speed, current):
   global leg_mode
   crawler.stand_position = crawler.stand_position + 1 & 1
   current = crawler.current_step_all_leg_value()
   
   left_backleg_move =  [
      ## [right front],[left front],[left rear],[right rear]
      
      # Lifts the left rear leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_START, X_TURN, Z_UP],[Y_START, X_DEFAULT, Z_DEFAULT]], 
      
      # move the left rear leg to the left
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT, Z_UP],[Y_START, X_DEFAULT, Z_DEFAULT]],
      
      # Put down the left rear leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT,Z_DEFAULT],[Y_START, X_DEFAULT, Z_DEFAULT]],
      
      # Move the rest legs to the leg
      [[Y_DEFAULT*2.5, X_DEFAULT, Z_DEFAULT],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      # [[Y_DEFAULT-30, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_START, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Lift the right front leg up
      [[Y_DEFAULT*2.5, X_DEFAULT, Z_UP],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT]],
      # [[Y_DEFAULT-30, X_DEFAULT, Z_UP],[Y_DEFAULT, X_START, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT]],
      
      # Move the right front leg to the left
      [[X_START, Y_DEFAULT, Z_UP],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # # Put down the right front rear leg
      [[X_START, X_TURN, Z_DEFAULT],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
   ]
   
   
   left_frontleg_move =  [
      
      # Lifts the left front leg
      [[X_START, X_TURN, Z_DEFAULT],[Y_START, X_TURN, Z_UP],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # move the left front leg to the left
      [[X_START, X_TURN, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT, Z_UP],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Put down the left front leg
      [[X_START, X_TURN, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Move the rest legs to the leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_START, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT, Z_DEFAULT]],
      
      # Lift the right back leg up
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_START, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT, Z_UP]],
      
      # Move the right back leg to the left
      [[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_START, X_DEFAULT, Z_DEFAULT],[X_START, Y_DEFAULT, Z_UP]],
      
      # # Put down the right back leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[X_START, X_DEFAULT, Z_DEFAULT],[Y_START, X_DEFAULT, Z_DEFAULT]], 
   ]
   
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
   
   
def move_sideRight(speed, current):
   global leg_mode
   
   stand(speed, current)
   crawler.stand_position = crawler.stand_position + 1 & 1
   current = crawler.current_step_all_leg_value()
   
   right_backleg_move =  [
      
      # Lifts the right rear leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_START, X_DEFAULT, Z_DEFAULT],[Y_START, X_TURN, Z_UP]], 
      
      # move the right rear leg to the left
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_START, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT, Z_UP]],
      
      # Put down the right rear leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_START, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT,Z_DEFAULT]],
      
      # Move the rest legs to the leg
      [[X_START, Y_DEFAULT, Z_DEFAULT], [Y_DEFAULT*2.5, X_DEFAULT, Z_DEFAULT], [Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Lift the left front leg up
      [[X_START, Y_DEFAULT, Z_DEFAULT], [Y_DEFAULT*2.5, X_DEFAULT, Z_UP], [Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT]],
      
      # Move the left front leg to the left
      [[X_START, Y_DEFAULT, Z_DEFAULT], [X_START, Y_DEFAULT, Z_UP], [Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # # Put down the left front rear leg
      [[X_START, Y_DEFAULT, Z_DEFAULT], [X_START, X_TURN, Z_DEFAULT], [Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
   ]
   
   
   right_frontleg_move =  [
      
      # Lifts the right front leg
      [[Y_START, X_TURN, Z_UP], [X_START, X_TURN, Z_DEFAULT], [Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # move the right front leg to the left
      [[Y_DEFAULT*2.5, X_DEFAULT, Z_UP], [X_START, X_TURN, Z_DEFAULT], [Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Put down the right front leg
      [[Y_DEFAULT*2.5, X_DEFAULT, Z_DEFAULT], [X_START, X_TURN, Z_DEFAULT], [Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT]],
      
      # Move the rest legs to the leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT, Z_DEFAULT], [X_START, Y_DEFAULT, Z_DEFAULT]],
      
      # Lift the left back leg up
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[Y_DEFAULT*2.5, X_DEFAULT, Z_UP],[X_START, X_DEFAULT, Z_DEFAULT]],
      
      # Move the left back leg to the left
      [[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_START, Y_DEFAULT, Z_UP],[X_START, X_DEFAULT, Z_DEFAULT]],
      
      # # Put down the left back leg
      [[Y_DEFAULT, X_DEFAULT, Z_DEFAULT],[X_DEFAULT, Y_DEFAULT, Z_DEFAULT],[Y_START, X_DEFAULT, Z_DEFAULT],[X_START, X_DEFAULT, Z_DEFAULT]], 
   ]
   
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

def move_rotateLeft(speed, current_pose):
   crawler.do_action('turn left', 1, speed)
   
def move_rotateRight(speed, current_pose):
   crawler.do_action('turn right', 1, speed)

def moveUp(speed, current):
   
   crawler.do_action('forward', 1, speed)

def moveDown(speed, current):
   crawler.do_action('backward', 1, speed)

def lookUp(speed, current):
   coords = [
      [[45, 45, -76], [45, 0, -76], [45, 0, -38], [45, 45, -30]],
   ]



   for coord in coords:
      crawler.do_step(coord, speed)


def lookDown(speed, current):
    coords = [
        # stand
        [[45, 45, -28], [45, 0, -40], [45, 0, -68], [45, 45, -76]],
    ]
    for coord in coords:
        crawler.do_step(coord, speed)

def get_local_ip(self):
   """Get local IP address"""
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.connect(("8.8.8.8", 80))
      return s.getsockname()[0]
   except:
      return "Unknown"
   
def start_server():
   # Run the mjpeg.py code to start video streaming
   # running other file using run()
   # subprocess.run(["python", "mjpeg.py"])
   os.system("python mjpeg.py")
   
   """ Start the server and listen for incoming connections. """
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
      server_socket.bind((HOST, PORT))
      server_socket.listen(5)
      # Recorded and print that the server has started listening for connection with client and store to a server log
      # logging.info(f"Server started and listening on {HOST}:{PORT}")
      print(f"Server started and listening on {HOST}:{PORT}")
      
      while True:
            try:
               # Accept new client connections and start a thread for each client
               client_socket, client_address = server_socket.accept()
               
               threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
            except Exception as e:
               # Records to the server log and prints if there has been an error on accepting connections
               # logging.error(f"Error accepting connections: {e}")
               print(f"Error accepting connections: {e}")
               
            current_pose = crawler.current_step_all_leg_value()
            crawler.do_step(current_pose, speed) # Attempt not avoid the robot to stay relaxed
               


def handle_client(client_socket, client_address):
   """ Handle incoming client requests. """
   # Recorded and print that the server has formed connection with a client and store to a server log
   # logging.info(f"Connection from {client_address}")
   print(f"Connection from {client_address}")
   
   try:
      while True:
         # Receive data from the client
         request_data = client_socket.recv(1024).decode("utf-8", errors="replace")
         if not request_data:  # Client has closed the connection
            break
            
         # Recorded the received request from the client and store to a server log
         # logging.info(f"Received request: {request_data} from {client_address}")
         # Print the received request from the client
         print(f"Received request: {request_data} from {client_address}")
         
         # Here, the request is processed to determine the response
         process_request(request_data, client_socket, client_address)
            
   except Exception as e:
         # print and log the error found while reading the client's data
         print(f"Error Found in Client's data: {e}")
         # logging.info(f"Error Found in Client's data: {e}")
         
   finally:
         # Close the client connection with grace
         client_socket.close()
         # Recorded and print that the client has close connection with the server and store to a server log
         # logging.info(f"Closed connection with {client_address}")
         print(f"Closed connection with {client_address}")         
            
def process_request(request_data, client_socket, client_address):
   """ Process the client's request and generate a response. """
   global speed
   current_pose = crawler.current_step_all_leg_value()
   if not request_data or request_data == "":
      client_socket.sendall("".encode("utf-8"))
      print(f"the request data is empty")
      # logging.info(f"the request data is empty")
      return

   elif 'left' == request_data: # move sideway left
      move_sideLeft(speed, current_pose)
   elif 'q' == request_data: # move sideway left
      move_rotateLeft(speed, current_pose)
      
   elif 'e' == request_data: # move sideway right
      move_rotateRight(speed, current_pose)
      
   elif 'right' == request_data: # move sideway right
      move_sideRight(speed, current_pose)
      
   elif 'r' == request_data: # move sideway right
      lookUp(speed, current_pose)
   elif 'f' == request_data: # move sideway right
      lookDown(speed, current_pose)
      
   elif 'up' == request_data: # move sideway right
      moveUp(speed, current_pose)
      
   elif 'down' == request_data: # move sideway right
      moveDown(speed, current_pose)
      
   elif 'stand' == request_data: # stand position
      crawler.do_step('stand', speed)
      
   elif '+' == request_data: # move sideway right
      speed+=5
      print(speed)
   elif '-' == request_data: # move sideway right
      speed-=5
      
   # else: # Assume it's audio
   #    while data != "":
   #       try:
   #             data = client_socket.recv(4096)
   #             stream.write(data)
   #       except socket.error:
   #             print("Client Disconnected")
   #             break
      

# If runs, the server starts
if __name__ == '__main__':
    start_server()
    
# after main close stop all audio processes
# stream.stop_stream()
# stream.close()
# p.terminate()