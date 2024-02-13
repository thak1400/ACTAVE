from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
from collections import Counter


def mood_label(video_path):
    face_classifier = cv2.CascadeClassifier(r'C:/ML Project/Flask Repo/haarcascade_frontalface_default.xml')
    classifier = load_model(r'C:/ML Project/Flask Repo/model.h5')
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
    mood_array = []
    list_ex =['Angry', 'Disgust', 'Fear', 'Surprise']
    cap = cv2.VideoCapture(video_path)
    
    # Get the video duration
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # Get total frames in the video
    
    while True:
        ret, frame = cap.read()
        if frame is None:
            break  # Break the loop if no frames are read
    
        labels = []
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)
    
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
    
            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
    
                prediction = classifier.predict(roi)[0]
                label = emotion_labels[prediction.argmax()]
                mood_array.append(label)
                
                label_position = (x, y)
                cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Close the video window after the specified duration

        cv2.imshow('Emotion Detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(mood_array)
    # Remove neutral moods from the array
    mood_array = [mood for mood in mood_array if mood not in list_ex]
    
    # Find the most common mood
    most_common_mood = Counter(mood_array).most_common(1)
    print(most_common_mood)
    
    if most_common_mood:
        print(f'Most common mood (excluding Neutral): {most_common_mood[0][0]}')
        return most_common_mood[0][0]
    else:
        print('No moods detected (excluding Neutral)')
        return None
    

