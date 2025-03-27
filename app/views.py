import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse, JsonResponse
from .llm import generate_responses_stream
from .models import Inquiry


def index(request):
    return render(request, "app/index.html")


@csrf_exempt
def generate(request):
    if request.method != "POST":
        return JsonResponse({"error": "Bad request."}, status=400)
    
    data = json.loads(request.body)

    # Filter out any empty lines from the prompt
    content = '\n'.join(filter(lambda line: line.strip() != '', data.get('content').split('\n')))
    rounds = 3 + int(data.get('numInsights', '1')) * 2
    
    # Save the inquiry in the database
    inquiry = Inquiry(prompt=content, rounds=rounds)
    inquiry.save()
    
    def event_stream():
        for chunk in generate_responses_stream(initial_prompt=content, rounds=rounds):
            yield chunk
    
    # Set the content type to text/event-stream for streaming
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
