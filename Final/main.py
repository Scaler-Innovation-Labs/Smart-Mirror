import cv2
import speech_recognition as sr # pip install SpeechRecognition
import threading

listener = sr.Recognizer()

# Type annotation shorthands
_camera_frame = cv2.typing.MatLike

# Variables
camera_open: bool = True

def take_command() -> str:
    command: str = ""
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if command.startswith("hey mirror"):
                command = command.replace("hey mirror", '')
                return command

    except Exception as e:
        print(e)

def process_speech() -> None:
    command = take_command()
    if command: print(command)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)  # Open default camera (0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        camera_open = False

    while camera_open:
        ret, frame = cap.read()  # Read a frame from the camera
        frame = cv2.flip(frame, 1)
        
        if not ret:
            print("Error: Could not read frame.")
            break

        if threading.active_count() == 1: threading.Thread(target=process_speech, daemon=True).start()
        
        cv2.imshow("Camera Feed", frame)  # Display the frame
        
        if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to exit
            break

    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close all OpenCV windows