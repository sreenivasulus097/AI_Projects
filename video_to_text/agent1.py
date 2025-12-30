import os
import subprocess
import whisper

# -----------------------------
# Tool: YouTube Downloader (yt-dlp)
# -----------------------------
def download_youtube_audio(url: str, output_file="temp_audio.mp3") -> str:
    print("Downloading audio from YouTube...")

    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", output_file,
        url
    ]

    subprocess.run(command, check=True)
    print(f"Downloaded audio as {output_file}")
    return output_file


# -----------------------------
# Tool: Whisper Transcriber
# -----------------------------
class VideoTranscriber:
    def __init__(self, model_name="base"):
        print("Loading Whisper model...")
        self.model = whisper.load_model(model_name)

    def transcribe(self, media_path: str) -> str:
        print(f"Transcribing: {media_path}")
        result = self.model.transcribe(media_path)
        return result["text"]


# -----------------------------
# Agent Core
# -----------------------------
class Agent:
    def __init__(self):
        self.tools = {}

    def register_tool(self, name, func):
        self.tools[name] = func

    def run(self, task_name, *args):
        if task_name not in self.tools:
            return f"❌ Tool '{task_name}' not found"
        return self.tools[task_name](*args)


# -----------------------------
# Utility
# -----------------------------
def save_text(text: str, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)


# -----------------------------
# Main CLI
# -----------------------------
if __name__ == "__main__":
    agent = Agent()
    transcriber = VideoTranscriber()

    agent.register_tool("transcribe", transcriber.transcribe)

    print("\n=== Agentic AI CLI ===")
    print("Supports:")
    print("- Local video/audio files")
    print("- YouTube URLs\n")

    user_input = input("Enter video path or YouTube URL: ").strip()

    # Decide input type
    if user_input.startswith("http"):
        media_path = download_youtube_audio(user_input)
    else:
        if not os.path.exists(user_input):
            print("❌ File not found")
            exit(1)
        media_path = user_input

    transcript = agent.run("transcribe", media_path)

    output_file = input("Enter output text file name: ").strip()
    save_text(transcript, output_file)

    print(f"\n✅ Transcript saved to {output_file}")
