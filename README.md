# listen
full stack for Listen

**Built for HackUCI 2019 | Won Best Overall Hack**

Link: https://devpost.com/software/listen

## Inspiration

As students in the modern age, we are inspired to combat the inefficiency of finding specific information in long audio samples. In a recorded math lecture, for example, only certain sections may be relevant to what you are trying to review. However, unlikelong text passages, there is no “command-F” that can be used to jump to the exact content needed in audio and video files. Thus, we have created an application that works as a search function for audio clips by transcribing and timestamping each spoken word.



## What it does

Just like the find function for web pages, PDFs, and other documents, our website implements the **“command-F” functionality for audio files**. The website allows for **precise scrubbing of audio** by prompting the user to search for a word and allowing them to **freely jump between occurrences of the word in the audio and play the file from that location**. The website also processes the file and extracts the **top five keywords** it believes the user will find most helpful to jump to using **Google Cloud’s Natural Language Processing API**. These suggestions act as probable topics of interests that potentially serve as **valuable points of reference** to the user.


## How we built it
The web application relies primarily on the Google Cloud Speech-to-Text API to asynchronously transcribe audio to text while also storing the timestamp of each word. This data is stored in a Python Dictionary with the words acting as keys and a list of timestamps of the word’s occurrence as the value.. To construct the relevant suggestions that the program offers, the Google Cloud Natural Language Processing API is used to identify words from the audio with high levels of “salience.” Promoting words with higher salience over sheer frequency, we prevent the inclusion of filler or common words.

### APIs Used
1. Google Cloud Speech
2. Google Cloud Storage
3. Google Cloud Datastore
2. Google Cloud Natural Language
3. Google Cloud  App Engine


The front-end is two styled HTML pages, one where the user can upload a file and one where the user can see the results. When the user uploads a file, we store it in the Google Cloud Storage Datastore using an API call. A python endpoint on our Flask server (described below) then processes the audio file and returns a list of keywords and a dictionary mapping each word to a list of its start times in the audio. Next, when the user tries to search for a specific word in the audio, the program will retrieve a list containing the start times of that word in the audio and allow the user to toggle between each one, very similar to the “command-F” functionality.

## Challenges we ran into

Although the NL API provides salience scores, some manipulations had to take place in order to make them useable. While working with the API, we were faced with the decision of whether or not to remove stopwords from the text. Stopwords are short words such as “the, at, on” which provide no real significance to the meaning of the sentence. Many NLP algorithms remove stop words to better analyze phrases.

For our project, we run the NL API on two sets of the audio transcripts: one containing stopwords and one with stopwords removed. This is because, as we were testing our algorithm, we noticed the API produced significantly different results for keywords depending on whether stop words were included. Since we believed both runs had useful outputs, our final output for salience takes the top five salient words from both algorithms combined.


## Accomplishments that we're proud of

We successfully built an application that solved a tangible issue we found. With little to no experience with APIs, we were proud to be able to create a working product using three of the Google Cloud APIs.
Flask server and connect
Query Cloud datastore
Deploy first Google App Engine

## What we learned

Over the course of 36 hours, our skills improved dramatically. We learned how to build the entire pipeline starting with creating a Google Cloud account to deploying the finished product on the Google App Engine. We also learned how to build a full stack application and integrate the front-end and back-end into a working application. Additionally, we learned how to implement control flow in HTML using Jinja2.


## What's next for Listen

One functionality we wanted to implement but didn’t have time for was built-in sound file conversion. Currently, our program only works with .flac files and we have to run two shell commands on any other sound type file to get it to fit our requirements. Our goal for the future is to be able to call these shell commands from within the program after the user uploads a file before it is sent to the cloud storage.

We are also hoping for embedded YouTube video functionality. Instead of uploading a sound file, the user can paste a link to a YouTube video. Our software would extract the audio and process it and allow the user to essentially search the video for the word they want.
Finally, our current implementation only allows for single-word search in the audio file. A relatively simple but largely helpful update would be to allow the user to search for phrases within the audio.
