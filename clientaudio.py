# Source - https://stackoverflow.com/q/54385072
# Posted by charlesalexanderlee, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-06, License - CC BY-SA 4.0

import socket
import pyaudio

# Socket
# HOST = socket.gethostname()
# !! Change into the Robot's IP when testing with the group5 SD card
HOST = "172.17.10.218" # Raspy's with CPSC584 wifi
PORT = 5001

# Audio
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording")

with socket.socket() as client_socket:
    client_socket.connect((HOST, PORT))
    while True:
        data = stream.read(CHUNK)
        client_socket.send(data)
