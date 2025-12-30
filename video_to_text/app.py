import whisper
import os

VIDEO_FILE = "Original_recording5.mp4"
OUTPUT_FILE = "transcript.txt"


def transcribe_video(video_path: str) -> str:
    """
    Converts video/audio file to text using Whisper
    """
    print("Loading Whisper model...")
    model = whisper.load_model("base")

    print("Transcribing...")
    result = model.transcribe(video_path)

    return result["text"]


def save_text(text: str, file_path: str):
    """
    Saves transcript to a text file
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    if not os.path.exists(VIDEO_FILE):
        print(f"❌ File not found: {VIDEO_FILE}")
        exit(1)

    transcript_text = transcribe_video(VIDEO_FILE)
    save_text(transcript_text, OUTPUT_FILE)

    print(f"✅ Transcript saved to {OUTPUT_FILE}")
