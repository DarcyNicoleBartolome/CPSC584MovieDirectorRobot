# Source - https://stackoverflow.com/a/54392055
# Posted by charlesalexanderlee, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-06, License - CC BY-SA 4.0

import socket
import pyaudio

# Socket
# HOST = socket.gethostname()
# !! Change into the Robot's IP when testing with the group5 SD card
# HOST = "172.17.10.218" # Raspy's with CPSC584 wifi
HOST = "127.0.0.1" # localhost
PORT = 5001

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

def print_audio_devices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"Index: {i}, Name: {info['name']}")
print_audio_devices()

with socket.socket() as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    print("Connection from " + address[0] + ":" + str(address[1]))

    data = conn.recv(4096)
    while data != "":
        try:
            data = conn.recv(4096)
            stream.write(data)
        except socket.error:
            print("Client Disconnected")
            break


stream.stop_stream()
stream.close()
p.terminate()
