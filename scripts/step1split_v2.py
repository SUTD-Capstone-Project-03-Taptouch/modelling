import argparse
import os
import time
import tracemalloc
import ffmpeg
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from pydub.silence import split_on_silence
from pydub.utils import make_chunks

# file locations for input and output audio
INPUT_PATH = "rawaudio"
OUTPUT_PATH = "splitaudio"

# useful global variables
DEFAULT_DURATION = 3000
# DEFAULT_FILETYPE = ".wav" yeah let's not
SILENCE_DUR = 3000  # for how long should there be no sound before it's considered a silent segment
SILENCE_THRESH = -40  # this number is very finicky: most song files have threshold at -24. online sources say -40
PAD_MS = 500  # librosa throws a hissy fit if you give it nothing


# def split_audio(duration, filetype):
# for future signalling, returns 0 if chunk is completely silent, else returns 1
def split_audio(duration=DEFAULT_DURATION, thresh=SILENCE_THRESH):
    for root, dirs, files in os.walk(INPUT_PATH):
        start_time = time.time()
        # tracemalloc.start()
        for filename in files:
            count = 1
            name, extension = os.path.splitext(filename)
            print("Found " + filename)
            if extension == ".wav":
                audio = AudioSegment.from_wav(INPUT_PATH + "/" + filename)
                print("Splitting for silence.")
                segments = split_on_silence(audio, SILENCE_DUR, thresh, keep_silence=500, seek_step=25)
                print("Splitting complete!")
                namepath = make_dir_if_not_exist(name)
                # print(len(segments))
                if len(segments) > 0:
                    for segment in segments:
                        # TODO: Test this on real conversational audio
                        print("Making chunks!")
                        chunks = make_chunks(segment, duration)
                        for i, chunk in enumerate(chunks, start=count):
                            chunk_name = namepath + "/" + name + "_chunk_{0}.wav".format(i)
                            print("Exporting: " + chunk_name)
                            chunk = pad_for_librosa(chunk)
                            chunk.export(chunk_name, format="wav")  # this assumes the path exists
                            count = i + 1
                else:
                    # Check that chunk isn't COMPLETELY silent
                    # got_silence = detect_nonsilent(audio, SILENCE_DUR, thresh, seek_step=25)
                    if not segments:
                        print("This chunk is completely silent.")
                        # yield 0
                    else:
                        print("No silence detected, making chunks!")
                        chunks = make_chunks(audio, duration)
                        for i, chunk in enumerate(chunks, start=count):
                            chunk_name = OUTPUT_PATH + "/" + name + "_chunk_{0}.wav".format(i)
                            print("Exporting: " + chunk_name)
                            chunk = pad_for_librosa(chunk)
                            chunk.export(chunk_name, format="wav")  # this assumes the path exists
                            count = i + 1
        print("Total time taken:", time.time() - start_time)
        # current, peak = tracemalloc.get_traced_memory()
        # print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
        # tracemalloc.stop()


def pad_for_librosa(clip):
    if len(clip) > PAD_MS:
        return clip
    else:
        silence = AudioSegment.silent(duration=PAD_MS-len(clip)+1)
        print("This clip was too short for librosa so we padded it just a bit.")
        padded = clip + silence
        return padded


def make_dir_if_not_exist(name):
    namepath = OUTPUT_PATH + "/" + name
    if not os.path.exists(namepath):
        os.makedirs(namepath)
    return namepath


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="step1split", description="""Splits audio into defined segments.""")
    parser.add_argument("-d", "--duration", help="(Optional) How long you want your audio segments to be (in "
                                                 "seconds). If unspecified, defaults to 3s.")
    parser.add_argument("-t", "--threshold", help="(Optional) Minimum threshold before segment is considered silent. "
                                                  "If unspecified, defaults to -40dBFs.")
    # parser.add_argument("-f", "--filetype", help="Audio format, e.g. \".mp3\". Defaults to .wav if not specified.")

    args = parser.parse_args()

    DURATION = int(args.duration) * 1000 if args.duration else DEFAULT_DURATION
    THRESH = args.threshold if args.threshold else SILENCE_THRESH
    # FILETYPE = args.filetype if args.filetype else DEFAULT_FILETYPE
    # split_audio(DURATION, FILETYPE)
    split_audio(DURATION, THRESH)
