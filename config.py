# NOTE: Some config parameters can be overrited by using command line arguments

# Download
# The size is in bytes, 314572800 = 300MB
max_allowed_size = 314572800

download_output_dir = "downloads"

# Time to wait when downloading in loop, ie: (Download everything in the room,
# Wait 60 seconds, Download everything in the room, and so on), note: each file
# it's only downloaded if the file wasn't downloaded before
download_loop_delay = 60

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
# For development it's beter to set the "driver_headless" to False, to show
# the window with the website.
driver_path = "drivers/chromedriver.exe"
driver_headless = True

# Logs
log_download_archive = True
log_download_error = True
log_download_too_big = True

# Chat
# The username must be between 3 and 12 characters
chat_logger_username = "mycooluser"
chat_logger_output_dir = "downloads"
