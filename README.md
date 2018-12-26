# Volafile Downloader

volafile.org files and chat downloader

Tested with **Python 3.6.2** on **Windows 10** (It should work anywhere).

## Install

Install all the required libraries:

```
pip install -r requirements.txt
```

Feel free to edit the config file with your own options, most of the stuff in there have comments with a little explanation. You don't have to edit it, it should work as is.

```
config.py
```

You need to have the chromium drivers, you can download the chromium drivers from their official website, go to http://chromedriver.chromium.org/downloads and download the drivers and place them in a directory, example: "drivers/**chromedriver.exe**".

If you are using **Linux**, **MacOS**, **other OS** or you have the chrome driver installed in other path, just change the path of the chromedriver in the config file. You might need to give permissions to the file, example: `sudo chmod +x chromedriver`

## Usage & Examples

Download all files from a room:

```
λ python volafile-downloader.py -r roomname
```

And with a password

```
λ python volafile-downloader.py -r roomname -p 123456
```

Download all files from a room and loops to check if new files were added (you can also change the time delay between the loop with the **-ld** option):

```
λ python volafile-downloader.py -r roomname -l
```

Download all files from a room and loops to check if new files were added and also downloads the chat logs (The download of chat logs only work with the download loop (-l argument), check the FAQ for more information)

```
λ python volafile-downloader.py -r roomname -l -cl
```

Download all files from a room with password and loops to check if new files were added and archives the files by creation date:

```
-r  : Room name
-p  : Room password
-l  : Loops to check for new files
-a  : Archives
-at : Archive type CREATION_DATE (Default) OR DOWNLOAD_DATE
-cl : Downloads the chat logs
```

```
λ python volafile-downloader.py -r roomname -p 123456 -l -a -at CREATION_DATE -cl
```

Show all the available options:  
Note: Some options/arguments will override some config variables.

```
λ python volafile-downloader.py -h
usage: volafile-downloader.py [-h] [-o OUTPUT_DIR] [-l] [-p PASSWORD] [-a]
                              [-at ARCHIVE_TYPE] [-cl] [-ld LOOP_DELAY]
                              [-ms MAX_ALLOWED_SIZE] [-nl] -r ROOM

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output directory
  -l, --loop            Download all the files in the room and loops to check
                        if new files were added
  -p PASSWORD, --password PASSWORD
                        Room password
  -a, --archive         Archive room
  -at ARCHIVE_TYPE, --archive-type ARCHIVE_TYPE
                        Archive type CREATION_DATE or DOWNLOAD_DATE
  -cl, --chat-log       Download chat log
  -ld LOOP_DELAY, --loop-delay LOOP_DELAY
                        Time delay when downloading in loop
  -ms MAX_ALLOWED_SIZE, --max-allowed-size MAX_ALLOWED_SIZE
                        Max allowed size to download a file (in bytes)
  -nl, --no-logs        Disable the logging to text files when a file is
                        downloaded, it's too big and when there was an error

required arguments:
  -r ROOM, --room ROOM  Room
```

## FAQ (Frequently asked questions)

**Where can I download the drivers?**

You can download the drivers from the official chromium website http://chromedriver.chromium.org/downloads

**Why I only can download the chat log with the loop argument (-l)?**

Because when you enter a room you don't have access to the chat messages that were sent before you entered the room, unless you were in the room when the other people sent the message. I believe the messages are not being saved in the Volafile servers and only are being send and received by Web Sockets and then saved in your computer.

## Feel free to buy me a coffee

Other Methods: <a href="https://www.buymeacoffee.com/H7KZCLEbG" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

Bitcoin (BTC): **12hPw1663w6Ne71g5zU1gFTjPh2syUTbeq**

Ethereum (ETH): **0x25b9318c17ef4f27b960c89bb90b855f09aa299f**

Litecoin (LTC): **LVwr7RhcdkTGTAgoy6iyxGrZKXvmE293HH**

Ripple (XRP): **12hPw1663w6Ne71g5zU1gFTjPh2syUTbeq**

## License

Copyright 2018 the-okn3

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
