import cv2

# Type annotation shorthands
_camera_frame = cv2.typing.MatLike

# Variables
camera_open: bool = True

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
        
        cv2.imshow("Camera Feed", frame)  # Display the frame
        
        if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to exit
            break

    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close all OpenCV windows