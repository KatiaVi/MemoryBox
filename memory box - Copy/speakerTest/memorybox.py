#####################################
#IDeATe Media Synthesis and Analysis -- Final Project (Empathy and Enviro)
#Vidhart Bhatia,  Angelo Pagliuca, Katia Villevald, Wynne Yao, Amy Wu

#Emotion Speech Analysis - Amy Wu, Vidhart Bhatia
#Google Speech API, PyAudio, Indico.io Emotion Analyis API
#####################################

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from pydub import AudioSegment
import wave
import indicoio
import io, time, os
from tkinter import *
import shutil
import random
import threading

def init(data):
    # load data.xyz as appropriate
    data.game = 0
    data.maxTime = 5
    data.timer = data.maxTime
    data.timePassed = 0
    data.updateNeeded = False
    data.record = "record"
    data.stop = 0

def writeFile(path, contents):
	with open(path, "wt") as f:
		f.write(contents)
#record
def runEmotionAnalyzer(data, timer):
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 16000
	RECORD_SECONDS = data.timer
	WAVE_OUTPUT_FILENAME = "output.wav"

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
	                channels=CHANNELS,
	                rate=RATE,
	                input=True,
	                frames_per_buffer=CHUNK)

	print("* recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)

	print("* done recording")

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

	sound1 = AudioSegment.from_wav("output.wav")
	sound1 = sound1.set_channels(1)
	sound1.export("output1.wav", format="wav")

	#transcribe (code from Rebecca Hong)
	transcript=""
	# Instantiates a client
	client = speech.SpeechClient()
	with io.open("output1.wav", 'rb') as audio_file:
		content = audio_file.read()
		audio = types.RecognitionAudio(content=content)
	config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')
	response = client.recognize(config, audio)
	for result in response.results:
		transcript+=str(result.alternatives[0].transcript)

	print(transcript)

	AudioSegment.from_wav("output.wav").export("output.mp3", format="mp3")


	indicoio.config.api_key = 'cf5bcb42cfe87a1a370bc95662ac0dee'

	emotionDict = indicoio.emotion(transcript)
	maxEmote = -1
	bestEmote = None
	joyEmote = -1
	for i in emotionDict:
		if (i == "joy"): joyEmote = emotionDict[i]
		if (i != "surprise" and emotionDict[i] > maxEmote):
			bestEmote = i
			maxEmote = emotionDict[i]

	if joyEmote > .15: bestEmote = "joy"
	print(bestEmote)

	writeFile("emotion.txt", bestEmote)

	dest = "data/%s/%s%d.mp3" % \
			(bestEmote, bestEmote, random.randint(0, 10000))
	shutil.move("output.mp3", dest)


def mousePressed(event, canvas, data):
    # use event.x and event.y
    if data.game == 0:
    	if ((data.width/4 <= event.x) and (event.x <= 3*data.width/4)
    		and (2*data.height/3-50 <= event.y) and (event.y <= 2*data.height/3+50)):
    		data.game = 1
    		data.updateNeeded = True
    		data.record = "recording"
    		redrawAll(canvas, data)
    		runEmotionAnalyzer(data, data.timer)
    		data.record = "record"
    		data.stop = 0
    		# d1 = threading.Thread(name = "runEmotionAnalyzer", target = runEmotionAnalyzer())
    		# d1.setDaemon(True)
    		# d1.start()

def keyPressed(event, canvas, data):
    # use event.char and event.keysym
    if data.game == 0:
    	if (event.keysym == "Enter"):
    		data.game = 1
    		data.updateNeeded = True
    		data.record = "recording"
    		redrawAll(canvas, data)
    		runEmotionAnalyzer(data, data.timer)
    		data.record = "record"
    		data.stop = 0
    		# d2 = threading.Thread(name = "runEmotionAnalyzer", target = runEmotionAnalyzer(data, data.timer))
    		# d2.setDaemon(True)
    		# d2.start()

def timerFired(data):
	if data.game == 1:
	    data.timePassed += 1
	    if data.timePassed % 10 == 0:
	    	data.timer -= 1
	    if data.timer == 0:
	    	data.timer = data.maxTime
	    	data.game = 0

def drawSplashScreen(canvas, data):
	# if data.record == "recording":
	# 	print("fuck this")
	canvas.create_rectangle(0, 0, data.width, data.height, fill = "black")
	canvas.create_text(data.width/2, data.height/2-25, text = "the memory room", fill = "white", font = "Helvetica 20")
	canvas.create_rectangle(data.width/4, 2*data.height/3-50, 
							3*data.width/4, 2*data.height/3+50, 
							outline = "white", fill = "black")
	canvas.create_text(data.width/2, 3*data.height/4-10, text = str(data.maxTime)+" seconds", fill = "white", font = "Helvetica 12")
	canvas.create_text(data.width/2, 2*data.height/3-10, text = data.record, fill = "white", font = "Helvetica 20")
	canvas.create_text(data.width/2, 3*data.height/4+30, text = "**please speak clearly and try not to use past tense", font = "Helvetica 10", fill="white")

# def drawRecord(canvas, data):
# 	canvas.create_rectangle(0, 0, data.width, data.height, fill = "black")
# 	canvas.create_text(data.width/2, data.height/2, text = data.timer, fill="white")

def redrawAll(canvas, data):
	# if data.record == "recording":
	# 	print("fuck you")
	drawSplashScreen(canvas, data)
    # if data.game == 1:
    # 	drawRecord(canvas, data)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, canvas, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, canvas, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # t = threading.Thread(name = 'timerFiredWrapper', target = timerFiredWrapper(canvas, data))
    # # t.setDaemon(True)
    # t.start()
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 400)