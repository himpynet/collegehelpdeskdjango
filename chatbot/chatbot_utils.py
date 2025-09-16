from fuzzywuzzy import process
from .models import FAQ

def get_bot_response(user_message):
    faqs = FAQ.objects.all()
    questions = [faq.question for faq in faqs]

    matched_question, score = process.extractOne(user_message, questions)

    if score > 70:  # Threshold to control accuracy
        matched_faq = FAQ.objects.get(question=matched_question)
        return matched_faq.answer
    else:
        return "Sorry, I don't have an answer to that at the moment."
