from django.shortcuts import render
from Chatmodel import qa_retrieval

# Create your views here.

def home(request):
    return render(request,'home.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def get_answer(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question', None)

        # Dummy logic to generate a response
        if question:
            answer = generate_answer(question)
            return JsonResponse({'answer': answer})
        else:
            return JsonResponse({'error': 'Question not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def generate_answer(question):
    answer = qa_retrieval(question)
    # Dummy function to generate response based on the question
    # You should replace this with your own logic to generate meaningful answers
    return "{}".format(answer)

