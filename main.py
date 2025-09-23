from smart_mirror import SmartMirror

if __name__ == "__main__":
    """
    Main entry point for the Smart Mirror application.
    """
    try:
        mirror = SmartMirror()
        mirror.run()
    except Exception as e:
        print(f"A critical error occurred: {e}")