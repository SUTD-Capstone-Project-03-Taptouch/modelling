import sounddevice as sd
import signal
from scipy.io.wavfile import write

SAMPLE_RATE = 48000  # this is in kHz
DURATION = 30  # seconds
OUTPUT_PATH = "rawaudio"

# TODO: allow for external interrupts?
# TODO: cleanup?


class GracefulExiter:
    def __init__(self):
        self.state = False
        signal.signal(signal.SIGINT, self.change_state)

    def change_state(self, signum, frame):
        print("Exit flag set to True (Press again to exit now.)")
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.state = True

    def exit(self):
        return self.state


def record_audio():
    flag = GracefulExiter()
    counter = 0
    while True:
        print("Recording file {0}.".format(counter))
        recording = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=2)
        sd.wait()
        print("Recording complete, processing file {0}.".format(counter))
        write(OUTPUT_PATH + "/" + "recording_{0}.wav".format(counter), SAMPLE_RATE, recording)
        counter += 1
        # Make sure the final file records properly before it stops.
        if flag.exit():
            print("Terminating gracefully...")
            break
    print("Complete!")


if __name__ == "__main__":
    record_audio()
