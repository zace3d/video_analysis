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

    return JsonResponse(context, safe=False)