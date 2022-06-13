import argparse
import os
import time
import ffmpeg
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import make_chunks
# TODO: Figure out what to do about ffmpeg being pesky
# TODO: probably move the audio samples to their own "/audio" folder?
# It seems like bad practice to have data in the scripts folder.

# file locations for input and output audio
INPUT_PATH = "rawaudio"
OUTPUT_PATH = "splitaudio"

# useful global variables
DEFAULT_DURATION = 3000
# DEFAULT_FILETYPE = ".wav" yeah let's not
SILENCE_DUR = 3000  # for how long should there be no sound before it's considered a silent segment
SILENCE_THRESH = -40  # this number is very finicky: most song files have threshold at -24. online sources say -40


# def split_audio(duration, filetype):
def split_audio(duration):
    for root, dirs, files in os.walk(INPUT_PATH):
        start_time = time.time()
        for filename in files:
            count = 1
            name, extension = os.path.splitext(filename)
            print("Found " + filename)
            if extension == ".wav":
                audio = AudioSegment.from_wav(INPUT_PATH + "/" + filename)
                print("Splitting for silence.")
                segments = split_on_silence(audio, SILENCE_DUR, SILENCE_THRESH, keep_silence=500, seek_step=25)
                print("Splitting complete!")
                print(len(segments))
                if len(segments) > 0:
                    for segment in segments:
                        # no extra padding is done in this step since librosa can do it there
                        # TODO: Test this on real conversational audio
                        # TODO: Get the program to auto-delete files?
                        print("Making chunks!")
                        chunks = make_chunks(segment, duration)
                        for i, chunk in enumerate(chunks, start=count):
                            chunk_name = OUTPUT_PATH + "/" + name + "_chunk_{0}.wav".format(i)
                            print("Exporting: " + chunk_name)
                            chunk.export(chunk_name, format="wav")  # this assumes the path exists
                            count = i + 1
                else:
                    print("No silence detected, making chunks!")
                    chunks = make_chunks(audio, duration)
                    for i, chunk in enumerate(chunks, start=count):
                        chunk_name = OUTPUT_PATH + "/" + name + "_chunk_{0}.wav".format(i)
                        print("Exporting: " + chunk_name)
                        chunk.export(chunk_name, format="wav")  # this assumes the path exists
                        count = i + 1
        print(time.time() - start_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="step1split", description="""Splits audio into defined segments.""")
    parser.add_argument("-d", "--duration", help="How long you want your audio segments to be (in seconds). Defaults "
                                                 "to 3s.")
    # parser.add_argument("-f", "--filetype", help="Audio format, e.g. \".mp3\". Defaults to .wav if not specified.")

    args = parser.parse_args()

    DURATION = int(args.duration) * 1000 if args.duration else DEFAULT_DURATION
    # FILETYPE = args.filetype if args.filetype else DEFAULT_FILETYPE

    # split_audio(DURATION, FILETYPE)
    split_audio(DURATION)
