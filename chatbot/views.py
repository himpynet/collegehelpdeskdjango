from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from .models import ChatLog
from .chatbot_utils import get_bot_response

@csrf_exempt
def get_bot_response_view(request):
    data = json.loads(request.body)
    user_message = data.get('message')

    bot_response = get_bot_response(user_message)

    # Store chat log
    ChatLog.objects.create(user=User.objects.first(), user_message=user_message, bot_response=bot_response)

    return JsonResponse({'response': bot_response})

def chat_page(request):
    return render(request, 'chatbot/chat.html')
