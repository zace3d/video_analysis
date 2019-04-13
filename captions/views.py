from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . import helpers

# Create your views here.

@csrf_exempt
def video_captions(request, version):

    # Get video
    yt_video_id = request.GET['yt_video_id']

    # Extract captions from Youtube video
    response = helpers.transcript(yt_video_id)

    return JsonResponse(response, safe=False)