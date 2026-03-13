import json
from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from AIapp.ai.pipeline import run
from AIapp.application.transfer_service import TransferService
from AIapp.application.exceptions import BankingException


@login_required
def home_page(request):
    return render(request, "home.html", {
        "username": request.user.username
    })


@csrf_exempt
@require_POST
@login_required
def voice_api(request):

    audio = request.FILES.get("audio")
    if not audio:
        return JsonResponse({"error": "No audio file provided"}, status=400)

    # 🔹 Используем request:
    user = request.user
    idempotency_key = request.headers.get("Idempotency-Key")
    client_ip = request.META.get("REMOTE_ADDR")

    try:
        transcript, intent, response = run(audio, request)

        return JsonResponse({
            "transcript": transcript,
            "intent": intent,
            "response": response,
            "user": user.username,
            "client_ip": client_ip,
            "idempotency_key": idempotency_key
        })

    except BankingException as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_POST
@login_required
def confirm_2fa_api(request):

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    transaction_id = data.get("transaction_id")
    code = data.get("code")

    if not transaction_id or not code:
        return JsonResponse({"error": "Missing fields"}, status=400)

    # 🔹 Используем request
    user = request.user
    client_ip = request.META.get("REMOTE_ADDR")

    service = TransferService()

    try:
        message = service.confirm_2fa(transaction_id, code)

        return JsonResponse({
            "message": message,
            "user": user.username,
            "client_ip": client_ip
        })

    except BankingException as e:
        return JsonResponse({"error": str(e)}, status=400)