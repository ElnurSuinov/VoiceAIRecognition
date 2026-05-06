import os
import tempfile
import whisper

MODEL_NAME = "small"
_model = None


def _get_model():
    global _model
    if _model is None:
        _model = whisper.load_model(MODEL_NAME)
    return _model


class SpeechToText:

    def transcribe(self, audio) -> str:

        model = _get_model()

        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
            for chunk in audio.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            result = model.transcribe(tmp_path, language="en")
            return result["text"].strip()
        finally:
            os.remove(tmp_path)
