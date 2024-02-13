from textblob import TextBlob
from pydub import AudioSegment
import speech_recognition as sr

def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'confident'
    elif analysis.sentiment.polarity < 0:
        return 'nervous'
    else:
        return 'normal'

def analyze_audio_sentiment(audio_file):
    # Load the audio file using pydub
    audio = AudioSegment.from_file(audio_file, format="wav")

    # Perform speech-to-text on the audio
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    # Convert audio data to text
    try:
        text = recognizer.recognize_google(audio_data)
        # Analyze sentiment of the transcribed text
        tonality = analyze_sentiment(text)
        print(f'Tonality: {tonality}')

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    return tonality
