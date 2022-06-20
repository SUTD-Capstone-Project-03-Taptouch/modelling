import os
import logging
import argparse

log = logging.getLogger(__name__)


def cleandirs(pathdir, mode=0):  # 0: partial cleanup, 1: full cleanup
    errs = 0
    if not os.path.exists(pathdir):
        print("Path does not exist!")
        return -1
    if mode == 0:
        for file in os.listdir(pathdir):
            fullpath = pathdir + "/" + file
            try:
                if file.startswith("recording"):
                    os.remove(fullpath)
            except OSError as e:
                errs += 1
                log.error(e)
                continue
    elif mode == 1:
        for file in os.listdir(pathdir):
            fullpath = pathdir + "/" + file
            try:
                if file.endswith(".wav"):
                    os.remove(fullpath)
            except OSError as e:
                errs += 1
                log.error(e)
                continue
    else:
        print("Cleanup mode not specified.")
        log.error("Invalid cleanup mode")
        return -1
    if errs == 0:
        print("Cleaned up!")
        return 1
    else:
        print("Cleaned up with some errors.")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="utils_cleandirs", description="""Junk cleaning and processing.""")
    parser.add_argument("p", "path", help="Path to the directory to clean.")
    parser.add_argument("-m", "--mode", help="(Optional) Cleanup mode. 0: Does not clean up testing files. 1: Clean "
                                             "all audio files. Use with caution.")
    # parser.add_argument("-f", "--filetype", help="Audio format, e.g. \".mp3\". Defaults to .wav if not specified.")
    args = parser.parse_args()

    if args.mode:
        s = cleandirs(args.path, args.mode)
    else:
        s = cleandirs(args.path)
