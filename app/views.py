import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render

from .llm import generate_responses
from .models import Inquiry


def index(request):
    return render(request, "app/index.html")


@csrf_exempt
def generate(request):
    if request.method != "POST":
        return JsonResponse({"error": "Bad request."}, status=400)
    
    data = json.loads(request.body)
    print(data)
    
    # filter body to remove any unnecessary new lines
    content = '\n'.join(filter(lambda line: line.strip() != '', data.get('content').split('\n')))
    
    # Get number of rounds based on number of insights requested
    rounds = 3 + int(data.get('numInsights', '1')) * 2
    
    # Save this inquiry inside the database
    inquiry = Inquiry(
        prompt=content,
        rounds=rounds
    )
    inquiry.save()
    
    # Get the generated responses from the LLMs
    responses = generate_responses(initial_prompt=content, rounds=rounds)
    return JsonResponse({'responses' : responses}, safe=False)
