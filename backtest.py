import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

import io
import nltk
import requests
import json
from nltk.corpus import stopwords as sw
sws = set(sw.words('english'))

# Imports the Google Cloud client library
from google.cloud import speech #pip install google-cloud-speech
from google.cloud.speech import enums
from google.cloud.speech import types

import six
from google.cloud import language #pip install google-cloud-language
from google.cloud.language import enums as langenums
from google.cloud.language import types as langtypes

# Returns WordTimeMap AND string with total text
# Requires a flac audio file
def returnWordTimeMap(audiofile):
    wordTimeMap = {}
    totaltext = ""
    totaltext2 = ""
    # Instantiates a client

    uri = audiofile
    audio = {'uri': uri}

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='en-US',
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True)

    operation = client.long_running_recognize(config, audio)
    print('Waiting for operation to complete...')
    response = operation.result() #Set to something
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.

    for result in response.results:
        # The first alternative is the most likely one for this portion.
        alternative = result.alternatives[0]
        for word_info in alternative.words:
            word = str(word_info.word)
            totaltext += word + " "
            if not word.lower() in sws:
                totaltext2 += word + " "
                if word not in wordTimeMap:
                    wordTimeMap[word] = [word_info.start_time.seconds + word_info.start_time.nanos *1e-9]
                else:
                    wordTimeMap[word].append(word_info.start_time.seconds + word_info.start_time.nanos *1e-9)

    for word in wordTimeMap:
        value = wordTimeMap[word]
        print ("Word: " + str(word) + "\t\tStart Time: " + str(value))
    print (totaltext)
    return wordTimeMap, totaltext, totaltext2

# Uses Google Cloud NLP to extract 5 most important words in speech
# Returns a an array with [keyword, salience]
def returnKeyWords(text):
    client2 = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')
    document = langtypes.Document(
    content=text,
    type=langenums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    entities = client2.analyze_entities(document).entities

    num = 0
    temp = 0
    keywords = [[],[],[],[],[]]
    while num is not 5:
        if not entities[temp].name in keywords:
            keywords[num] = [str(entities[temp].name), entities[temp].salience]
            print('=' * 20)
            print(u'{:<16}: {}'.format('name', entities[temp].name))
            print(u'{:<16}: {}'.format('salience', entities[temp].salience))
            num += 1
        temp += 1
    return keywords

# Returns dictionary containing word to time map and top 5 keywords in speech
# Requires a .flac audio file
def returnWordTimeAndKeyWord(audiofile):
    wordTimeMap, y, z = returnWordTimeMap(audiofile)
    y = returnKeyWords(y)
    z = returnKeyWords(z)
    keyword = []
    keyword.extend(y[:2])
    keyword.extend(z[:2])
    if y[3][1] > z[3][1]:
        keyword.append(y[3])
    else:
        keyword.append(z[3])
    for x in keyword:
        print (x[0] + " " + str(x[1]))
    return wordTimeMap, keyword
