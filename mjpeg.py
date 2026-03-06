from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput
from http.server import BaseHTTPRequestHandler, HTTPServer
import io, threading

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

def main():
    picam2 = Picamera2()
    # You can change size/fps later
    picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
    picam2.start_recording(MJPEGEncoder(), FileOutput(output))

    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print("MJPEG stream:")
    print("  http://<PI_IP>:8080/stream.mjpg")
    print("  http://<PI_IP>:8080/  (preview page)")
    server.serve_forever()

if __name__ == "__main__":
    main()