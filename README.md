# Volafile Downloader
volafile.org files downloader

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

I have included the chrome driver, but if you don't trust me you can download it from https://sites.google.com/a/chromium.org/chromedriver/downloads and replace it in "drivers/**chromedriver.exe**"
If you are using **Linux**, **other OS** or you have the chrome driver installed in other path, just change the path of the chromedriver in the config file.

## Usage
Download all files from a room:
```
λ python download.py -r roomname
```

Download all files from a room and loops to check if new files were added (you can also change the time delay between the loop with the **-ld** option):
```
λ python download.py -r roomname -l
```

Show all the available options:  
Note: Some options/arguments will override some config variables.
```
λ python download.py --help

usage: download.py [-h] [-o OUTPUT_DIR] [-l] [-ld LOOP_DELAY]
                   [-ms MAX_ALLOWED_SIZE] [-nl] -r ROOM

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output directory
  -l, --loop            Download all the files in the room and loops to check
                        if new files were added
  -ld LOOP_DELAY, --loop-delay LOOP_DELAY
                        Time delay when downloading in loop
  -ms MAX_ALLOWED_SIZE, --max-allowed-size MAX_ALLOWED_SIZE
                        Max allowed size to download a file (in bytes)
  -nl, --no-logs        Disable the logging to text files when a file is
                        downloaded, it's too big and when there was an error

required arguments:
  -r ROOM, --room ROOM  Room
```

## Feel free to buy me a coffee
Bitcoin: **1LR1qvNufQo1NTmRamycFFvjumZ4zZjcfH**


## License
Copyright 2017 the-okn3

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
