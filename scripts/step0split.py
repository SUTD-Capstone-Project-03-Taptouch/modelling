import argparse
import os

RAWPATH = "rawaudio"
OUTPUTPATH = "splitaudio"


def split_audio(duration, filetype):
    for root, dirs, files in os.walk(RAWPATH):
        for filename in files:
            name, extension = os.path.splitext(filename)
            print(name, extension)
            if extension == filetype:
                print("True")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="step0split", description="""Splits audio into defined segments.""")
    parser.add_argument("--duration", help="How long you want your audio segments to be. Defaults to 3s.")
    parser.add_argument("--filetype", help="Audio format, e.g. \".mp3\". Defaults to .wav if not specified.")

    args = parser.parse_args()

    DURATION = int(args.duration) * 1000 if args.duration else 3000
    FILETYPE = args.filetype if args.filetype else ".wav"

    split_audio(DURATION, FILETYPE)

