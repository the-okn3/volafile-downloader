#!/usr/bin/env python

__author__ = "Okn3"
__email__ = "okn3@protonmail.com"
__license__ = "MIT"
__version__ = "2.0.0"

import sys
import config
import argparse
import logging
import colorlog

from downloader import Downloader


def get_args():
    """ Get and prepare all the arguments """

    parser = argparse.ArgumentParser()

    # Optional
    parser.add_argument("-o", "--output-dir", help="Output directory",
                        required=False, default=config.download_output_dir)

    parser.add_argument("-l", "--loop", action="store_true",
                        help="Download all the files in the room and "
                        "loops to check if new files were added")
    parser.add_argument("-p", "--password", default=None,
                        help="Room password")
    parser.add_argument("-a", "--archive", action="store_true",
                        default=config.archive,
                        help="Archive room")
    parser.add_argument("-at", "--archive-type", default=config.archive_type,
                        help="Archive type CREATION_DATE (Default) or "
                        "DOWNLOAD_DATE")
    parser.add_argument("-cl", "--chat-log", action="store_true",
                        default=config.chat_log,
                        help="Download chat log")
    parser.add_argument("-ld", "--loop-delay",
                        default=config.download_loop_delay,
                        help="Time delay when downloading in loop")
    parser.add_argument("-ms", "--max-allowed-size",
                        default=config.max_allowed_size,
                        help="Max allowed size to download a file (in bytes)")
    parser.add_argument("-nl", "--no-logs",
                        default=True, action="store_false",
                        help="Disable the logging to text files when a file "
                        "is downloaded, it's too big and when there was "
                        "an error")

    # Required
    required = parser.add_argument_group('required arguments')
    required.add_argument("-r", "--room", help="Room", required=True)

    return parser.parse_args()


def init_logger():
    """ Initialize the logger """
    global logger

    logger = logging.getLogger("root")
    logger.setLevel(config.logger_stream_level)

    # Stream Handler
    logger_stream_handler = colorlog.StreamHandler()
    logger_stream_handler.setLevel(config.logger_stream_level)
    logger_stream_formatter = colorlog.ColoredFormatter(
        config.logger_stream_format, datefmt=config.logger_stream_date_format)
    logger_stream_handler.setFormatter(logger_stream_formatter)

    logger.addHandler(logger_stream_handler)

    # File Handler
    if config.logger_file_active:
        logger_file_handler = logging.FileHandler(config.logger_file_path)
        logger_file_handler.setLevel(config.logger_file_level)
        logger_file_formatter = logging.Formatter(
            config.logger_file_format, datefmt=config.logger_file_date_format)
        logger_file_handler.setFormatter(logger_file_formatter)

        logger.addHandler(logger_file_handler)


def main():
    """ Main function that is executed when running the program """

    args = get_args()

    init_logger()

    global downloader
    downloader = Downloader(room=args.room,
                            password=args.password,
                            output_dir=args.output_dir,
                            max_allowed_size=args.max_allowed_size,
                            do_log=args.no_logs,
                            archive=args.archive,
                            archive_type=args.archive_type,
                            chat_log=args.chat_log)

    if args.loop:
        downloader.downloadLoop(args.loop_delay)
    else:
        downloader.download()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted by the user.")
        if downloader:
            downloader.stop()
        sys.exit()
