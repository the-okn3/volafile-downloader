#!/usr/bin/env python

__author__ = "Okn3"
__email__ = "okn3@protonmail.com"
__license__ = "MIT"
__version__ = "1.0.0"

import re
import os
import sys
import time
import requests
import humanfriendly
import config
import argparse

from tqdm import tqdm
from termcolor import colored
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support import ui
from utils import sanitize_file_name, prepare_url, log, get_file_id_and_name,\
    get_file_extension


def download_file(url, file_name=None):
    """ Downloads a file from volafile and shows a progress bar """

    chunk_size = 1024

    try:
        r = requests.get(url, stream=True, headers=config.headers,
                         cookies=config.cookies)
        r.raise_for_status()

        if not r:
            return False

        total_size = int(r.headers.get("content-length", 0))

        with open(file_name + ".part", "wb") as f:
            for data in tqdm(iterable=r.iter_content(chunk_size=chunk_size),
                             total=total_size / chunk_size, unit="KB",
                             unit_scale=True):
                f.write(data)

        # Remove the ".part" from the file name
        os.rename(file_name + ".part", file_name)

        return True
    except Exception as ex:
        print(colored("[-] Error: " + str(ex), "red"))
        return False


def get_files_list(room):
    """
    Get the list of files from a room and prepare the information of each file
    """

    if config.driver_path and not os.path.exists(config.driver_path):
        print(
            colored("[-] Error: The driver path in the config doesn't exist",
                    "red")
        )
        sys.exit(1)

    options = webdriver.ChromeOptions()
    if config.driver_headless:
        options.add_argument('headless')

    global driver

    driver = webdriver.Chrome(config.driver_path, chrome_options=options)
    wait = ui.WebDriverWait(driver, 10)

    driver.get(prepare_url(config.base_url, room))

    # Wait for +18 warning modal and click OK
    wait.until(lambda driver: driver.find_element_by_xpath(
        """//*[@id="room_content_fixed"]/div[1]/div/div[3]/span[2]""")).click()

    # Wait for the list of files and get them
    files = wait.until(lambda driver: driver.find_elements_by_css_selector(
        "#file_list .filelist_file"))

    # Get all files information
    files_list_output = []
    for file_elem in files:

        file_left_part = file_elem.find_element_by_class_name(
            "file_left_part")

        file_right_part = file_elem.find_element_by_class_name(
            "file_right_part")

        url = file_left_part.get_attribute("href")

        # custom_file_name = file_left_part.find_element_by_class_name(
        #     "file_name").get_attribute("innerHTML")
        # custom_file_name = sanitize_file_name(custom_file_name)

        file_tag = file_left_part.find_element_by_class_name(
            "file_tag").get_attribute("innerHTML")

        file_size_expiration = file_right_part.get_attribute("innerHTML")
        size_expiration_pattern = re.compile(r"^(.*?)<.*>(.*)<\/span>")
        size_expiration_info = size_expiration_pattern.findall(
            file_size_expiration)

        file_size = size_expiration_info[0][0]
        file_expiration = size_expiration_info[0][1]

        file_id, real_file_name = get_file_id_and_name(url)

        file_name_without_extension, extension = get_file_extension(
            real_file_name)

        files_list_output.append({
            "id": file_id,
            "url": url,
            "name": sanitize_file_name(file_name_without_extension),
            "extension": extension,
            "tag": file_tag,
            "size": humanfriendly.parse_size(file_size),
            "expiration": file_expiration
        })

    driver.close()
    driver.quit()

    return files_list_output


def download_room(room, output_dir, max_allowed_size=config.max_allowed_size,
                  do_log=True):
    """ Download all the files from an entire room """

    print(colored("[+] Room: %s\n" % (room), "blue"))

    download_directory = os.path.join(output_dir, room)
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    try:
        print(colored("[+] Downloading the list of files...", "blue"))
        files = get_files_list(room)
        print(colored("[+] List of files downloaded", "blue"))
    except Exception as ex:
        print(colored("[-] The Website might be offline or another error "
                      "occurred: " + str(ex), "red"))

        if driver:
            driver.close()
            driver.quit()

        sys.exit(0)

    total_files = len(files)
    total_files_downloaded = 0
    total_files_already_existed = 0
    total_files_too_big = 0
    total_files_error = 0
    total_files_extension_not_allowed = 0
    file_index = 1

    for f in files:

        print(colored("\n[%s of %s] [%s] [%s] [%s] [by %s]" % (
            file_index,
            total_files,
            f["name"],
            f["extension"],
            humanfriendly.format_size(f["size"]),
            f["tag"]
        ), "blue"))

        file_path = os.path.join(
            download_directory,
            f["name"] + " - " + str(f["id"]) + f["extension"]
        )

        if not os.path.exists(file_path):

            if not f["extension"] in config.extensions_blacklist:

                if not f["size"] > max_allowed_size:
                    print(colored("[+] Downloading...", "blue"))
                    downloaded = download_file(f["url"], file_path)

                    if not downloaded:
                        print(colored("[-] Error downloading", "red"))
                        if do_log:
                            log("ERROR", download_directory, f)
                        total_files_error += 1
                    else:
                        print(colored("[+] Downloaded", "green"))
                        if do_log:
                            log("ARCHIVE", download_directory, f)
                        total_files_downloaded += 1
                else:
                    print(colored("[~] File size not allowed to download",
                                  "red"))
                    if do_log:
                        log("TOOBIG", download_directory, f)
                    total_files_too_big += 1
            else:
                print(colored("[~] File Extension not allowed to download",
                              "red"))
                total_files_extension_not_allowed += 1
        else:
            print(colored("[~] File already exists", "blue"))
            total_files_already_existed += 1

        file_index += 1

    print(colored("\n[+] DONE", "blue"))
    print(colored("[+] %s of %s Files downloaded" %
                  (total_files_downloaded, total_files), "blue"))
    print(colored("[+] %s of %s Files already existed" %
                  (total_files_already_existed, total_files), "blue"))
    print(colored("[+] %s of %s Files were too big to download" %
                  (total_files_too_big, total_files), "blue"))
    print(colored("[+] %s of %s Files have extensions not allowed to "
                  "download" %
                  (total_files_extension_not_allowed, total_files), "blue"))
    print(colored("[+] %s of %s Files couldn't be downloaded (error "
                  "downloading)" %
                  (total_files_error, total_files), "blue"))


def get_args():
    """ Get and prepare all the arguments """

    parser = argparse.ArgumentParser()

    # Optional
    parser.add_argument("-o", "--output-dir", help="Output directory",
                        required=False, default=config.download_output_dir)

    parser.add_argument("-l", "--loop", action="store_true",
                        help="Download all the files in the room and "
                        "loops to check if new files were added")
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


def main():
    """ Main function that is executed when running the program """

    args = get_args()

    if args.loop:
        while True:
            print(colored("\n[%s]\n" % (
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')), "blue"))
            download_room(args.room, args.output_dir, args.max_allowed_size,
                          args.no_logs)
            print(colored("\n[Sleeping for %s seconds]\n" % (
                args.loop_delay), "blue"))
            time.sleep(args.loop_delay)
    else:
        download_room(args.room, args.output_dir, args.max_allowed_size,
                      args.no_logs)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\nInterrupted by the user.", "blue"))
        sys.exit()
