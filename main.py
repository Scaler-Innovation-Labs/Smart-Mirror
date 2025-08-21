from smart_mirror import SmartMirror

if __name__ == "__main__":
    mirror = SmartMirror()
    while mirror.active:
        mirror.run_once()
