import sounddevice as sd
import signal
import tracemalloc
from scipy.io.wavfile import write

SAMPLE_RATE = 48000  # this is in kHz
DURATION = 30  # seconds
OUTPUT_PATH = "rawaudio"


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


def record_audio(sample_rate=SAMPLE_RATE, duration=DURATION):
    flag = GracefulExiter()
    counter = 0
    while True:
        tracemalloc.start()
        print("Recording file {0}.".format(counter))  # TODO: Replace counter with timestamp?
        recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=2)
        sd.wait()
        print("Recording complete, processing file {0}.".format(counter))
        write(OUTPUT_PATH + "/" + "recording_{0}.wav".format(counter), sample_rate, recording)
        counter += 1
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
        tracemalloc.stop()
        # yield 1  # TODO: Fix implementation to allow for possible threadedness.
        # Make sure the final file records properly before it stops.
        if flag.exit():
            print("Terminating gracefully...")
            break
    print("Complete!")
    return 0


if __name__ == "__main__":
    record_audio()
