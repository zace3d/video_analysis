from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . import helpers

# Create your views here.

@csrf_exempt
def convert_video(request, version):

    # Get video
    video = request.FILES['video']

    # Transcribe video and extract audio
    response = helpers.transcribe_file(video)

    context = response

    # return render(request, 'api/v1/result_successful.html', context)
    return JsonResponse(context, safe=False)