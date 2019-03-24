import face_recognition
import cv2
from os import listdir

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

print("Init")
path = "carasConocidas/"

known_face_encodings = []
known_face_names = []

for file in listdir(path):
    image = face_recognition.load_image_file(path+file)
    known_face_encodings.append(face_recognition.face_encodings(image)[0])
    known_face_names.append(file.split(".")[0])
'''    
# Load a sample picture and learn how to recognize it.
alejo_image = face_recognition.load_image_file("carasConocidas/Alejo.jpg")
alejo_face_encoding = face_recognition.face_encodings(alejo_image)[0]

# Load a second sample picture and learn how to recognize it.
nano_image = face_recognition.load_image_file("carasConocidas/Nano.jpg")
nano_face_encoding = face_recognition.face_encodings(nano_image)[0]

alex_image = face_recognition.load_image_file("carasConocidas/Alex.jpg")
alex_face_encoding = face_recognition.face_encodings(alex_image)[0]

ivan_image = face_recognition.load_image_file("carasConocidas/Ivan.jpg")
ivan_face_encoding = face_recognition.face_encodings(ivan_image)[0]

fede_image = face_recognition.load_image_file("carasConocidas/Fede.jpg")
fede_face_encoding = face_recognition.face_encodings(fede_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    alejo_face_encoding,
    nano_face_encoding,
    alex_face_encoding,
    ivan_face_encoding,
    fede_face_encoding
]
known_face_names = [
    "Alejo",
    "Nano",
    "Alex",
    "Ivan",
    "Fede"
]
'''
def run(path):
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)



    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True


    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (180, 132, 109), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (180, 132, 109), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    #cv2.imshow('Video', frame)
    cv2.imwrite(path+"FotoPuerta.jpg", frame)

    # Hit 'q' on the keyboard to quit!

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    return face_names