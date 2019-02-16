import io
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Instantiates a client
client = speech.SpeechClient()

uri = 'gs://test75829/1min.ogg'
audio = {'uri': uri}

config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.OGG_OPUS,
    sample_rate_hertz=48000,
    language_code='en-US',
    enable_word_time_offsets=True)

#New stuff
operation = client.long_running_recognize(config, audio)
print('Waiting for operation to complete...')
response = operation.result(timeout=60) #Set to something

# Each result is for a consecutive portion of the audio. Iterate through
# them to get the transcripts for the entire audio file.
for result in response.results:
    # The first alternative is the most likely one for this portion.
    alternative = result.alternatives[0]
    print(u'Transcript: {}'.format(result.alternatives[0].transcript))
    print('Confidence: {}'.format(result.alternatives[0].confidence))
    for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9))

# Detects speech in the audio file OLD
# response = client.recognize(config, audio)
# print (response)
# for result in response.results:
#     print('Transcript: {}'.format(result.alternatives[0].transcript))
