import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render

from .llm import *
from .models import *


def index(request):
    return render(request, "app/index.html")


@csrf_exempt
def generate(request):
    if request.method != "POST":
        return JsonResponse({"error": "Bad request."}, status=400)
    
    # filter body to remove any unnecessary new lines
    content = '\n'.join(filter(lambda line: line.strip() != '', request.POST['body'].split('\n')))
    
    # Get number of rounds based on number of insights requested
    rounds = 3 + int(request.POST['num-insights']) * 2
    
    # Save this inquiry inside the database
    inquiry = Inquiry(
        prompt=content,
        rounds=rounds
    )
    inquiry.save()
    
    return JsonResponse(inquiry.serialize(), safe=False)
