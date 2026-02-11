from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .ai.pipeline import run
from pathlib import Path
from django.conf import settings
from .models import DialogueLog

# Create your views here.
@csrf_exempt
def home_page(request):
    if request.method == "POST" and request.FILES.get("audio"):
        audio_file = request.FILES["audio"]
        relative_path = default_storage.save("input.webm", audio_file)

        full_path = Path(settings.MEDIA_ROOT) / relative_path

        text, intent, response = run(str(full_path))

        DialogueLog.objects.create(
            user_text = text,
            intent = intent,
            ai_response = response
        )

        return JsonResponse({
            "transcript": text,
            "intent": intent,
            "response": response
        })

    return render(request, "home.html")

