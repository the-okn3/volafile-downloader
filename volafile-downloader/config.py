# NOTE: Some config parameters can be overwrite by using command line arguments

# Download
# The size is in bytes, 314572800 = 300MB
max_allowed_size = 314572800

download_output_dir = "../downloads"

chat_log = True
chat_messages_to_ignore = [
    """Volafile can also be found here: https://twitter.com/volafile https://facebook.com/volafile"""
]
chat_nicks_to_ignore = [
    "News"
]

# Archive will create and put the files in separated folders by date
# note: the date that is created is the date the file was added, so if the
# same file was added some other day and it was added again it will download
# again the file
# ex: <room_name>/2018-10-13
archive = False
# Archive types:
#     CREATION_DATE = The date the file was created
#     DOWNLOAD_DATE = The date the file was downloaded
archive_type = "CREATION_DATE"
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
archive_date_format = "%Y-%m-%d"

# Time to wait when downloading in loop, ie: (Download everything in the room,
# Wait 60 seconds, Download everything in the room, and so on), note: each file
# it's only downloaded if the file wasn't downloaded before
download_loop_delay = 60

# To start with the oldest files (that will expire first) first
download_oldest_first = True

# Extensions to not download
extensions_blacklist = [".mp3", ".wav"]

# This can be edited or removed, the only thing needed is the user-agent
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) "
    "Gecko/20100101 Firefox/55.0",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1"
}

# This shouldn't be edited or removed, it's required to download the files
cookies = {
    "allow-download": "1"
}

base_url = "https://volafile.org/r/"

# Driver
# For development it's better to set the "driver_headless" to False, to show
# the window with the website.
driver_path = "../drivers/chromedriver.exe"
driver_headless = True
driver_log_level = 3

# Logs
log_download_archive = True
log_download_error = True
log_download_too_big = True

logger_stream_format = "[%(asctime)s] %(log_color)s[%(levelname)s] - " \
    "%(message)s%(reset)s"
logger_stream_level = "DEBUG"
logger_stream_date_format = "%m-%d-%y %H:%M:%S"

logger_file_active = True
logger_file_format = "[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s"
logger_file_level = "INFO"
logger_file_date_format = "%m-%d-%y %H:%M:%S"
logger_file_path = "../downloads/volafile-downloader.log"
