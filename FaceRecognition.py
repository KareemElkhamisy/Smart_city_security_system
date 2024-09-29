import cv2
import face_recognition

# Load the known image of Kareem and encode it
known_image = face_recognition.load_image_file("kareem.jpg")
kareem_encoding = face_recognition.face_encodings(known_image)[0]

# Initialize the default camera
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    
    if not ret:
        print("Error: Failed to capture image.")
        break

    # Find all the faces and face encodings in the frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_location, face_encoding in zip(face_locations, face_encodings):
        # See if the face in the frame matches the known face of Kareem
        matches = face_recognition.compare_faces([kareem_encoding], face_encoding)
        print(matches)
        top, right, bottom, left = face_location

        # Draw a box around the face
        color = (0, 255, 0) if matches[0] else (255, 0, 0)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Label the face as Kareem or Unknown
        label = "Kareem" if matches[0] else "Unknown"
        cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
video_capture.release()
cv2.destroyAllWindows()
