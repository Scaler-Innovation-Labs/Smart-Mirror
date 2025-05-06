from hey_mirror import SmartMirror
import subprocess

def capture_image(image_path="/home/smart-mirror/Pictures/captured_image.jpg"):
    command = ["libcamera-still", "-o", image_path]
    try:
        subprocess.run(command, check=True)
        print(f"📸 Image captured successfully at: {image_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to capture image: {e}")

if __name__ == "__main__":
    mirror = SmartMirror()

    while True:
        transcript= mirror.run_once()
        if transcript:
            capture_image() 
            mirror.get_gpt_response(transcript)
