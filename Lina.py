import speech_recognition as sr
import pytz
import json
import random
import playsound
import os
import warnings
import wikipedia
import webbrowser

from datetime import date, datetime
from darksky.api import DarkSky
from darksky.types import languages, units, weather
from gtts import gTTS 
from PyDictionary import PyDictionary

# 1.Initialize
speech = sr.Recognizer() # recorder
today = date.today() # current date
dictionary = PyDictionary() # dictionary
warnings.filterwarnings('ignore') # ignore warnings

# init robot_brain
with open("knowledge.JSON") as file:
	robot_brain = json.load(file)

# get current time by timezone
tz_Hanoi = pytz.timezone('Asia/Ho_Chi_Minh') # timezone
datetime_Hanoi = datetime.now(tz_Hanoi) # current time

# darksky - daily weather
API_KEY = 'e2fea81b36c2588f1315c4ad2b721989' # This is OneMonth's api key (OneMonth.com)

darksky = DarkSky(API_KEY)

forecast = darksky.get_forecast( # get forecast for Hanoi
    21.0294498, # latitude
    105.8544441, # longitude 
    extend=False, # default `False`
    lang=languages.ENGLISH, # default `ENGLISH`
    # units=units.AUTO, # default `auto`
    exclude=[weather.MINUTELY, weather.ALERTS] # default `[]`
)


# 2.Define fundamental function
def getRequest(ask): # record user's voice
	with sr.Microphone() as mic:
		print(ask)
		audio = speech.listen(mic)

	try:
		return speech.recognize_google(audio)
	except: # google can't recognize the content of the audio
		return "" 

def verbalize(res): # robot responses by speaking
	myobj = gTTS(text=res, lang='en', slow=False) 
	myobj.save("output.mp3") # Convert text to speech and save as mp3 file
	print("robot: " + robot_response)
	playsound.playsound('output.mp3') # Play the converted file 
	os.remove("output.mp3")

def checkPattern(req): # check if robot can answer this question base on "hard" knowledge
	for intent in robot_brain['intents']:
		for pattern in intent['patterns']:
			if pattern in req:
				return intent
	return robot_brain['intents'][0]


# 3.Make conversation
while True:
	# obtain audio from the microphone
	you = getRequest("Say something!!!") # catch voice
	print("You said: " + you)

	# robot's response
	if you == "":
		robot_response = "I can't hear you! Please try again"
	
	elif you == "ok" or you == "okay" or you == "okay fine":
		robot_response = "okay!"
	
	elif "today" in you:
		if "weather" in you:
			robot_response = "Current temperature is " + str(forecast.currently.temperature) + "\n"
			robot_response += "In the next few hour, " + forecast.hourly.summary + '\n'
			robot_response += "And this week will be " + forecast.daily.summary
		else:
			robot_response = "Today is " + today.strftime("%B %d, %Y")
	
	elif "time" in you:
		robot_response = datetime_Hanoi.strftime("%H hours %M minutes %S seconds")
	
	elif "what does" in you and "mean" in you:
		wordSpl = you.split(' ')
		word = dictionary.meaning(wordSpl[-2])
		if word is None:
			robot_response = "I can't not find it in the dictionary"
		else:
			robot_response = "Check out what I have found"
			for wordType, meanings in word.items():
				print(wordType + ": ")
				for meaning in meanings:
					print("    - " + meaning)
	
	elif "search for" in you:
		search = you.split('search for ')[-1]
		try:
			overallInfo = wikipedia.summary(search, sentences=2)
			print(overallInfo)
			print("URL: " + wikipedia.page(search).url)
			robot_response = "Here's what I found"
		except:
			robot_response = "I can't find any information related to " + search + " with Wikipedia! Try to search it yourself."
	
	elif "find location of" in you:
		place = you.split("find location of ")[-1]
		url = "http://google.nl/maps/place/" + place + "/&amp"
		webbrowser.get().open(url)
		robot_response = "Here's where I found for " + place
	
	elif "stop" in you:
		verbalize("Okay! Bye")
		break
	
	elif "thank you" in you or "thanks" in you:
		ans = ["No problem!", "You're welcome", "I'm glad to help you!"]
		robot_response = random.choice(ans)
	
	else:
		intent = checkPattern(you)
		robot_response = random.choice(intent['responses'])
		if intent['tag'] == "ending": # i.e. bye bye
			verbalize(robot_response)
			break

	# verbal response
	print("Pending...")
	verbalize(robot_response) # robot speaks
