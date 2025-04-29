from hey_mirror import SmartMirror
import subprocess

def capture_image(image_path="/home/captured_image.jpg"):
    command = ["libcamera-still", "-o", image_path]
    try:
        subprocess.run(command, check=True)
        print(f"📸 Image captured successfully at: {image_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to capture image: {e}")

if __name__ == "__main__":
    mirror = SmartMirror()

    while True:
        transcript, response = mirror.run_once()
        if transcript and response:
            capture_image()  # Only capture after full interaction
