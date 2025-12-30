import os
import whisper

# -----------------------------
# Tool: Video Transcriber
# -----------------------------
class VideoTranscriber:
    def __init__(self, model_name="base"):
        print("Loading Whisper model...")
        self.model = whisper.load_model(model_name)

    def transcribe(self, video_path: str) -> str:
        if not os.path.exists(video_path):
            return f"❌ Video file not found: {video_path}"
        print(f"Transcribing video: {video_path}")
        result = self.model.transcribe(video_path)
        return result["text"]

# -----------------------------
# Agent Core
# -----------------------------
class Agent:
    def __init__(self):
        self.tools = {}

    def register_tool(self, name: str, func):
        """Register a new tool/skill"""
        self.tools[name] = func

    def run_task(self, task_name: str, *args, **kwargs):
        """Run the selected tool with arguments"""
        if task_name not in self.tools:
            return f"❌ Tool '{task_name}' not available."
        return self.tools[task_name](*args, **kwargs)

# -----------------------------
# Helper to save text
# -----------------------------
def save_text(text: str, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

# -----------------------------
# Main CLI
# -----------------------------
if __name__ == "__main__":
    agent = Agent()

    # Register Video Transcription Tool
    transcriber = VideoTranscriber()
    agent.register_tool("transcribe_video", transcriber.transcribe)

    print("=== Agent CLI Prototype ===")
    print("Available tasks:", list(agent.tools.keys()))
    task_name = input("Enter task: ").strip()

    if task_name == "transcribe_video":
        video_path = input("Enter video path: ").strip()
        transcript = agent.run_task(task_name, video_path)
        if transcript.startswith("❌"):
            print(transcript)
        else:
            output_file = input("Enter output text file name (e.g., transcript.txt): ").strip()
            save_text(transcript, output_file)
            print(f"✅ Transcript saved to {output_file}")
    else:
        result = agent.run_task(task_name)
        print(result)
