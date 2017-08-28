import os
import re
import config

from termcolor import colored
from urllib.parse import unquote
from os.path import splitext


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
        print(colored("[-] Error: Fix the god damn code, there is a log "
                      "type that doesn't exist: " + log_type.upper(), "red"))
        return

    if output_path:
        message = "%s - %s - %s - %s - %s\n" % (file_info["url"],
                                                file_info["name"],
                                                file_info["tag"],
                                                file_info["size"],
                                                file_info["expiration"])

        with open(output_path, "a+", encoding="utf-8") as f:
            f.write(str(message))


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
