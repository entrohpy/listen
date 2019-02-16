import io
import os

import requests
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def returnWordTimeMap(audiofile): #currently doesn't work
    # Instantiates a client
    client = speech.SpeechClient()
    #Start converting file to mono flac
    os.system("ftransc -f flac " + audiofile)
    os.system("ffmpeg -i " + audiofile + " -ac 1 " + audiofile[:len(audiofile) - 5] + "mono.flac"
    #End converting file

    uri = 'gs://test75829/9min.flac'
    #uri = 'gs://python-docs-samples-tests/speech/audio.flac'
    audio = {'uri': uri}

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='en-US',
        enable_word_time_offsets=True)

    #New stuff
    operation = client.long_running_recognize(config, audio)
    print('Waiting for operation to complete...')
    response = operation.result() #Set to something
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    wordTimeMap = []
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        alternative = result.alternatives[0]
        #print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        #print('Confidence: {}'.format(result.alternatives[0].confidence))
        for word_info in alternative.words:
            wordTimeMap.append((word_info.word, word_info.start_time))
            # word = word_info.word
            # start_time = word_info.start_time
            # end_time = word_info.end_time
            # print('Word: {}, start_time: {}, end_time: {}'.format(
            #     word,
            #     start_time.seconds + start_time.nanos * 1e-9,
            #     end_time.seconds + end_time.nanos * 1e-9))
    for key, value in wordTimeMap:
        print ("Word: " + str(key) + "\t\t'Start Time: " + str(value.seconds + value.nanos * 1e-9))
    # Detects speech in the audio file OLD
    # response = client.recognize(config, audio)
    # print (response)
    # for result in response.results:
    #     print('Transcript: {}'.format(result.alternatives[0].transcript))
