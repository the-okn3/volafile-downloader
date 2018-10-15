import os
import re
import config
import requests

from tqdm import tqdm
from urllib.parse import unquote
from os.path import splitext
from datetime import datetime, timedelta


def sanitize_file_name(file_name):
    """
    Sanitize a file name by removing extra spaces, replaces spaces with
    underscores and escapes special characters
    """

    file_name = str(file_name).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', file_name)


def log(log_type, path, file_info):
    """ Log information to a file """

    output_path = None

    if log_type.upper() == "ERROR" and config.log_download_error:
        output_path = os.path.join(path, "error.txt")

    elif log_type.upper() == "ARCHIVE" and config.log_download_archive:
        output_path = os.path.join(path, "archive.txt")

    elif log_type.upper() == "TOOBIG" and config.log_download_too_big:
        output_path = os.path.join(path, "toobig.txt")

    else:
        print("[-] Error: Fix the god damn code, there is a log "
              "type that doesn't exist: " + log_type.upper())
        return

    if output_path:
        message = "%s - %s - %s - %s - %s\n" % (file_info["url"],
                                                file_info["name"],
                                                file_info["tag"],
                                                file_info["size"],
                                                file_info["expiration"])

        with open(output_path, "a+", encoding="utf-8") as f:
            f.write(str(message))


def log_file(file_path_as_id, path):
    output_path = os.path.join(path, "files.txt")
    with open(output_path, "a+", encoding="utf-8") as f:
        f.write(str(file_path_as_id) + "\n")


def get_logged_files(path):
    output_path = os.path.join(path, "files.txt")
    if not os.path.exists(output_path):
        return []

    with open(output_path, "r", encoding="utf-8") as f:
        # splitlines will remove the '\n' in the end and return a list of line.
        return set(f.read().splitlines())
    return []


def prepare_url(base_url, room):
    """ Prepare a URL by adding the room to the base URL """

    if not base_url.endswith("/") and not room.startswith("/"):
        base_url += "/"
    elif base_url.endswith("/") and room.startswith("/"):
        base_url = base_url[:-1]

    return base_url + room


def get_file_id_and_name(url):
    """ Get the file id and name from a URL """

    pattern = re.compile(r"\/get\/([a-zA-Z0-9-_]+)\/(.*)")
    info = pattern.findall(url)
    file_id = info[0][0]
    file_name = unquote(info[0][1])
    return file_id, file_name


def get_file_extension(file_name):
    """ Get the file extension from a file name """

    for ext in ['.tar.gz', '.tar.bz2']:
        if file_name.endswith(ext):
            return file_name[:-len(ext)], file_name[-len(ext):]
    return splitext(file_name) or ""


def download_file(url, file_name=None):
    """ Downloads a file from Volafile and shows a progress bar """

    chunk_size = 1024

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


def expiration_to_date(expiration):
    expiration = expiration.lower().strip()
    number, method = expiration.split(" ")
    max_expiration_days = 2
    date = datetime.now() + timedelta(days=-max_expiration_days)
    number = int(number)

    if method == "day" or method == "days":
        return date + timedelta(days=+number)
    elif method == "hour" or method == "hours":
        return date + timedelta(hours=+number)
    elif method == "min" or method == "mins":
        return date + timedelta(minutes=+number)
    elif method == "sec" or method == "secs":
        return date + timedelta(seconds=+number)

    return datetime.now()
