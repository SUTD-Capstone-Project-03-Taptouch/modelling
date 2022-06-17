import os
import logging
import argparse

log = logging.getLogger(__name__)


def cleandirs(pathdir):
    errs = 0
    if not os.path.exists(pathdir):
        print("Path does not exist!")
        return 0
    for file in os.listdir(pathdir):
        fullpath = pathdir + "/" + file
        try:
            if file.endswith(".wav"):
                os.remove(fullpath)
        except OSError as e:
            errs += 1
            log.error(e)
            continue
    if errs == 0:
        print("Cleaned up!")
        return 1
    else:
        print("Cleaned up with some errors.")
        return -1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="utils_cleandirs", description="""Junk cleaning and processing.""")
    parser.add_argument("-p", "--path", help="Clean up after yourself.")
    # parser.add_argument("-f", "--filetype", help="Audio format, e.g. \".mp3\". Defaults to .wav if not specified.")
    args = parser.parse_args()

    s = cleandirs(args.path)
