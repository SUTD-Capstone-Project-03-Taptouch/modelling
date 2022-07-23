import librosa
import numpy as np
import os

SAMPLE_RATE = 48000  # this is in kHz
DURATION = 3
OFFSET = 0.5
INPUT_PATH = "splitaudio"
# OUTPUT_PATH = "processedaudio"
# Note: This is for Shaya's Colab Notebook.


def librosafy():
    all_signals = []
    directories = []
    for root, subdirs, files in os.walk(INPUT_PATH):
        for subdir in subdirs:
            directories.append(os.path.join(root, subdir))
    for directory in directories:
        for i, subdirs, files in os.walk(directory):
            signals = []
            for j, file in enumerate(files):
                audio, sample_rate = librosa.load(directory + "/" + file, duration=DURATION,
                                                  offset=OFFSET, sr=SAMPLE_RATE)
                signal = np.zeros((int(SAMPLE_RATE * 3, )))
                signal[:len(audio)] = audio
                signals.append(signal)
                print("\r Processed {}/{} files:".format(j+1, len(files)), end=" ")
                print(file)
            if signals:
                signals = np.stack(signals, axis=0)
                all_signals.append(signals)
    print("\n", all_signals)
    print("I have converted " + str(len(all_signals)) + " samples.")
    return all_signals


if __name__ == "__main__":
    librosafy()
