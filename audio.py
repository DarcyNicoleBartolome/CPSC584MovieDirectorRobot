"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
import sys
import numpy

FORMAT = pyaudio.paInt16
CHANNELS = 1
# RATE = 16000
OUTPUT_SAMPLE_RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 6

def generate_sample(self, ob, preview):
    print("* Generating sample...")
    tone_out = numpy.array(ob, dtype=numpy.int16)

    if preview:
        print("* Previewing audio file...")

        bytestream = tone_out.tobytes()
        pya = pyaudio.PyAudio()
        stream = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=OUTPUT_SAMPLE_RATE, output=True)
        stream.write(bytestream)
        stream.stop_stream()
        stream.close()

        pya.terminate()
        print("* Preview completed!")
    else:
        write('sound.wav', SAMPLE_RATE, tone_out)
        print("* Wrote audio file!")