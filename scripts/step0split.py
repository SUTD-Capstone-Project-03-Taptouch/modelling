import argparse
import os
import time
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import make_chunks
from pydub.silence import detect_silence
# TODO: Figure out what to do about ffmpeg being pesky

# file locations for input and output audio
RAWPATH = "rawaudio"
OUTPUTPATH = "splitaudio"

# useful global variables
DEFAULT_DURATION = 3000
DEFAULT_FILETYPE = ".wav"
SILENCE_DUR = 3000  # for how long should there be no sound before it's considered a silent segment
SILENCE_THRESH = -24  # this number is hella finicky. originally was 16.


# def split_audio(duration, filetype):
def split_audio(duration):
    for root, dirs, files in os.walk(RAWPATH):
        start_time = time.time()
        for filename in files:
            count = 1
            name, extension = os.path.splitext(filename)
            print("Found " + filename)
            if extension == ".wav":
                audio = AudioSegment.from_wav(RAWPATH + "/" + filename)
                # no extra padding is done in this step since librosa can do it there
                # i just want to see if it splits because silence detection is wonky
                print("Making chunks!")
                chunks = make_chunks(audio, duration)
                for i, chunk in enumerate(chunks, start=count):
                    chunk_name = OUTPUTPATH + "/chunk_{0}.wav".format(i)
                    print("Exporting: " + chunk_name)
                    chunk.export(chunk_name, format="wav")  # this assumes the path exists
                    count = i + 1
        print(time.time() - start_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="step0split", description="""Splits audio into defined segments.""")
    parser.add_argument("-d", "--duration", help="How long you want your audio segments to be (in seconds). Defaults "
                                                 "to 3s.")
    # parser.add_argument("-f", "--filetype", help="Audio format, e.g. \".mp3\". Defaults to .wav if not specified.")

    args = parser.parse_args()

    DURATION = int(args.duration) * 1000 if args.duration else DEFAULT_DURATION
    # FILETYPE = args.filetype if args.filetype else DEFAULT_FILETYPE

    # split_audio(DURATION, FILETYPE)
    split_audio(DURATION)
