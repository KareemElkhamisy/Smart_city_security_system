import cv2
import face_recognition
import RPi.GPIO as GPIO
from time import sleep
from mfrc522 import SimpleMFRC522
GPIO.setwarnings(False)    # Ignore warning for now

def openGate():
    angle=180
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT)
    pwm=GPIO.PWM(27, 50)
    pwm.start(0)
    duty = angle / 18 + 2
    GPIO.output(27, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(27, False)
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup()

def closeGate():
    angle=1
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT)
    pwm=GPIO.PWM(27, 50)
    pwm.start(0)
    duty = angle / 18 + 2
    GPIO.output(27, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(27, False)
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup()

def RFgate ():

    
    GPIO.setmode(GPIO.BOARD)

    reader = SimpleMFRC522()
    while True:
            try:

                id, text = reader.read()
                print(id)
                if id== 388369945219:
                    CAMVERIFY=FACERECO()
                   

                else :
                    print ("RF VERIFY Acess denied")    
            
                sleep(2)
                
                    
            except:
                GPIO.cleanup()

def FACERECO():   
        
    # Load the known image of Kareem and encode it
    known_image = face_recognition.load_image_file("kareem.jpg")
    kareem_encoding = face_recognition.face_encodings(known_image)[0]

    # Initialize the default camera
    video_capture = cv2.VideoCapture(0)
    result=False
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
            result=matches[0]
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
    video_capture.release()
    cv2.destroyAllWindows()
    if result==True:
        print('Access Graunted')
        openGate()
        closeGate()
    else:
        print('FACEID Acess Denied')    
    return result


             

def main():                
     RFgate()

main()