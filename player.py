import os
import sys
import random
import vlc
import time
import select
import requests
from bs4 import BeautifulSoup

class Player:
	'''
	Functions are self explanatory.
	'''
	def __init__(self, address):
		self.address = address
		self.musicFiles = []

	def scanDirectory(self):
		# Traverses for all '.mp3' files
		for root, dirs, files in os.walk(self.address):
			for file in files:
				if file.endswith(".mp3"):
					self.musicFiles.append(os.path.join(root, file))

	def shuffle(self):
		# The list gets mixed randomly
		self.musicFiles = random.sample(self.musicFiles, len(self.musicFiles))

	def getLyrics(self):
		# azlyrics' urls have a property of being made of:
		# artist name followed by song name in small case and without spaces
		url = "https://www.azlyrics.com/lyrics/"
		artist = input("Enter artist/band name : ").replace(" ","").lower()
		song = input("Enter song name : ").replace(" ","").lower()
		url = url + str(artist) + "/" +str(song) + ".html"

		open_url = None

		try:
			open_url = requests.get(url, timeout=5)
		except:
			print("Connection refused by the server.. - " + url)
			time.sleep(10)

		if(open_url != None):
			soup = BeautifulSoup(open_url.content, 'html.parser')
			lyrics = str(soup.find_all('div', class_='col-xs-12 col-lg-8 text-center'))

			# The lyrics are before and after the following text : 
			start = lyrics.find('Sorry about that. -->')+21
			end = lyrics.find('</br></br></br></br></br>')

			lyrics = (lyrics[start:end]).replace('<br>','').replace('<i>', '').replace('</i>', '')
			print(lyrics)

	def getArtistInfo(self):
		url = "https://en.wikipedia.org/wiki/"
		artist = str(input("Enter artist name: "))
		url = url + artist

		open_url = None

		try:
			open_url = requests.get(url, timeout=5)
		except:
			print("Connection refused by server.. - " + url)
			time.sleep(10)

		if(open_url != None):
			soup = BeautifulSoup(open_url.content, 'html.parser')
			info = soup.find_all('p')
			print(info[1].text.strip())

	def playSongQueue(self):
		pos = 0
		
		# While loop is necessary as we will have to traverse backwards in case user clicks 'r' - previous
		while(pos < len(self.musicFiles)):
			song = self.musicFiles[pos]
			pos += 1;
			
			print('Now Playing: '+song[len(self.address):])
			
			now = vlc.MediaPlayer(song)

			# Song starts to play
			now.play()
			
			# We need a time delay before we get duration else it produces 0
			time.sleep(1.5)
			
			duration = now.get_length()/1000

			print("Duration: "+str(duration) + " seconds")
			
			# Counter starts to check for autoplay condition
			start = time.time()
			
			menu = 'PRESS n - next | s - shuffle | r - previous| l -lyrics | a - artist info | p - Pause | h - help | e - exit--followed by ENTER'
			print(menu)

			# The while condition checks for the song to finish condition
			while((time.time() - start) <= duration):
				# Checks for a user input for 1 sec, if no input it refreshes
				i, o, e = select.select( [sys.stdin], [], [], 1)
				if(i):
					inp = sys.stdin.readline().strip()
				else:
					continue	

				if(inp == 'n'):
					break

				elif(inp == 'r'):
					pos -= 2
					break
				
				elif(inp == 's'):
					self.shuffle()
					break
				
				elif(inp == 'l'):
					self.getLyrics()			
				
				elif(inp == 'a'):
					self.getArtistInfo()

				elif(inp == 'p'):
					now.pause()
				
				elif(inp == 'e'):
					sys.exit(0)
				
				elif(inp == 'h'):
					print(menu)	

			print()

			now.stop()

if __name__ == '__main__':
	address = './songs/'
	obj = Player(address)
	obj.scanDirectory()
	obj.shuffle()
	obj.playSongQueue()