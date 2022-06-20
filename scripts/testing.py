from pydub import AudioSegment
import time


def make_test():
    long_silence = AudioSegment.silent(duration=30000, frame_rate=48000)
    long_silence.export("rawaudio/sample2.wav", format="wav")


def test_yield():
    while True:
        print("Hello!")
        time.sleep(3)
        yield 1


if __name__ == "__main__":
    for i in test_yield():
        print("Hi! ", i)
