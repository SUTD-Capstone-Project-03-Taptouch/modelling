import librosa
import numpy as np
import os

SAMPLE_RATE = 48000  # this is in kHz
DURATION = 3
OFFSET = 0.5
INPUT_PATH = "splitaudio"
# OUTPUT_PATH = "processedaudio"


def librosafy():
    signals = []
    for root, dirs, files in os.walk(INPUT_PATH):
        for i, file in enumerate(files):
            audio, sample_rate = librosa.load(INPUT_PATH + "/" + file, duration=DURATION, offset=OFFSET, sr=SAMPLE_RATE)
            signal = np.zeros((int(SAMPLE_RATE * 3, )))
            signal[:len(audio)] = audio
            signals.append(signal)
            print("\r Processed {}/{} files.".format(i, len(files)), end=" ")
    signals = np.stack(signals, axis=0)
    print("\n", signals)
    print("I have converted " + str(len(signals)) + " files.")
    return signals


if __name__ == "__main__":
    librosafy()
