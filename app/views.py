import os
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse, JsonResponse
from .llm import generate_responses_stream
from .models import *


def index(request):
    return render(request, "app/index.html")


@csrf_exempt
def generate(request):
    if request.method != "POST":
        return JsonResponse({"error": "Bad request."}, status=400)
    
    content = request.POST.get('content', '').strip()
    file = request.FILES.get('docfile')
    rounds = 3 + int(request.POST.get('rounds', '')) * 2

    uploaded_file_path = None
    if file:
        newdoc = Document(docfile=file)
        newdoc.save()
        uploaded_file_path = os.path.join(settings.MEDIA_ROOT, newdoc.docfile.name)

    print(f"Content: {content}")
    print(f"Uploaded File: {uploaded_file_path if file else 'No file uploaded'}")
    
    def event_stream():
        for chunk in generate_responses_stream(initial_prompt=content, rounds=rounds, file_path=uploaded_file_path):
            yield chunk
    
    # Set the content type to text/event-stream for streaming
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')