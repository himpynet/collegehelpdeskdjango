from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from transformers import pipeline # type: ignore
from .models import FAQ, ChatLog
from django.contrib.auth.models import User

qa_pipeline = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')

@csrf_exempt
def get_bot_response(request):
    data = json.loads(request.body)
    user_message = data.get('message')

    context = "Admissions process, library timings, fees structure of the college..."

    result = qa_pipeline(question=user_message, context=context)

    if result['score'] > 0.5:
        bot_response = result['answer']
    else:
        # Fallback to FAQ matching
        faqs = FAQ.objects.all()
        bot_response = "Sorry, I don't have an answer for that."

        for faq in faqs:
            if user_message.lower() in faq.question.lower():
                bot_response = faq.answer
                break

    # Store chat log (Optional: link to authenticated user)
    ChatLog.objects.create(user=User.objects.first(), user_message=user_message, bot_response=bot_response)

    return JsonResponse({'response': bot_response})
