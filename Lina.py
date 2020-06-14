import speech_recognition as sr
import pytz
import json
import random
import playsound
import os

from datetime import date, datetime
from darksky.api import DarkSky
from darksky.types import languages, units, weather
from gtts import gTTS 

# 1.Initialize
speech = sr.Recognizer() # recorder
today = date.today() # current date

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
def getRequest(): # record user's voice
	with sr.Microphone() as mic:
		print("Say something!")
		audio = speech.listen(mic)

	try:
		return speech.recognize_google(audio)
	except: # google can't recognize the content of the audio
		return "" 

def verbalize(res): # robot responses by speaking
	print("Pending...")
	myobj = gTTS(text=res, lang='en', slow=False) 
	myobj.save("output.mp3") # Convert text to speech and save as mp3 file
	print("robot: " + robot_response)
	playsound.playsound('output.mp3') # Play the converted file 

def checkPattern(req): # check if robot can answer this question base on "hard" knowledge
	for intent in robot_brain['intents']:
		for pattern in intent['patterns']:
			if pattern in req:
				return intent
	return robot_brain['intents'][0]


# 3.Make conversation
while True:
	# obtain audio from the microphone
	you = getRequest() # catch voice
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
	else:
		intent = checkPattern(you)
		robot_response = random.choice(intent['responses'])
		if intent['tag'] == "ending": # i.e. bye bye
			verbalize(robot_response)
			break

	# verbal response
	verbalize(robot_response) # robot speaks

if os.path.exists("output.mp3"):
	os.remove("output.mp3")