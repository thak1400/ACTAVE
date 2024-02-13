from flask import Flask, request, jsonify,render_template,redirect,url_for 
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import main as mood_recognition
import tonal as tonalityrecognition
import model_prediction as mp

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_audio(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_text = recognizer.record(source)
            text = recognizer.recognize_google(audio_text)
            return text
    except UnknownValueError:
        return "Speech not recognized"
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/templates/survey.html')
def survey():
    return render_template('survey.html')

@app.route('/save_answers', methods=['POST'])
def save_answers():
    global stored_answers
    data = request.json
    answers = data.get('answers', [])
    
    # Process the answers as needed
    print('Received answers:', answers)

    # Store answers globally (this is just an example, consider using a database)
    stored_answers = answers

    return jsonify({'message': 'Answers received successfully'})

@app.route('/templates/fileUpload.html')
def upload():
    return render_template('fileUpload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global stored_answers
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = "uploadedVideo.mp4"
    
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Extract audio from the video
        video_clip = VideoFileClip(filepath)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'audio.wav')
        video_clip.audio.write_audiofile(audio_path)

        # Extract text from the audio
        text = extract_text_from_audio(audio_path)

        video_path = r'C:/ML Project/Flask Repo/uploads/uploadedVideo.mp4'
        audio_path = r'C:/ML Project/Flask Repo/uploads/audio.wav'
        mood = mood_recognition.mood_label(video_path)
        tonality = tonalityrecognition.analyze_audio_sentiment(audio_path)
        x=0
        y=[text]
        for i in stored_answers:
            x+=int(i)
            y.append(int(i))
        y.append(x)
        y.append(tonality)
        y.append(mood)
        print(y)
        val =[y]
        print("Value is "+str(val)) 
        value = mp.anxiety_calc(val)
        if(value==0):
            level_of_anxiety = "Minimal Anxiety"
        elif(value==1):
            level_of_anxiety = "Mild Anxiety"
        elif(value==2):
            level_of_anxiety = "Moderate Anxiety"
        else:
            level_of_anxiety = "Severe Anxiety"

        return redirect(url_for('result', text=text, mood=mood, tonality=tonality, GAD_Score=x, Anxiety_Level=level_of_anxiety))


    return jsonify({'error': 'Invalid file format'})

@app.route('/result')
def result():
    # Retrieve values from the URL parameters or request.args
    text = request.args.get('text')
    mood = request.args.get('mood')
    tonality = request.args.get('tonality')
    GAD_Score = request.args.get('GAD_Score')
    Anxiety_Level = request.args.get('Anxiety_Level')

    # Render the result template only when the required data is available
    if text and mood and tonality and GAD_Score and Anxiety_Level:
        return render_template('result.html', text=text, mood=mood, tonality=tonality, GAD_Score=GAD_Score, Anxiety_Level=Anxiety_Level)
    else:
        return redirect(url_for('loading'))


@app.route('/loading')
def loading():
    return render_template('loading.html')

if __name__ == '__main__':
    app.run(debug=True)
