# music-player
**A command line based music player application**

This application works only on LINUX and MAC OS.

It performs basic operations like **shuffle**, **pause** ,**forward**, **backward**, **fetch lyrics** and **artist info**.

## How to run the code
You first have to install python-vlc module using:
```
pip3 install python-vlc
```

To download beautifulSoup use:
```
pip3 install beautifulsoup4
```

In the main method replace the address with your music folder's file path.

You can then run the code using:
```
python3.5 player.py
```

I have used **https://azlyrics.com** to scrape lyrics. If you are facing issues with lyrics, try searching for proper artist name.
eg:  https://azlyrics.com/lyrics/thebeatles won't work
	 https://azlyrics.com/lyrics/beatles will work.