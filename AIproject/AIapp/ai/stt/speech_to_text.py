import whisper

model = whisper.load_model("base")

class SpeechToText:
    def transcribe(self, audio_path: str) -> str:
        result = model.transcribe(audio_path)
        return result["text"]