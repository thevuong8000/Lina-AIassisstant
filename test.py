# Import the Gtts module for text  
# to speech conversion 
from gtts import gTTS 
import playsound
  
mytext = 'Convert this Text to Speech in Python'
  
# Language we want to use 
language = 'en'
  

myobj = gTTS(text=mytext, lang='en', slow=False) 
myobj.save("output.mp3") 
  
# Play the converted file 
playsound.playsound('output.mp3')