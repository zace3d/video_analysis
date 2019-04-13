import io
import os
import environ

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaIoBaseDownload

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def transcript(yt_video_id):
    env = environ.Env(DEBUG=(bool, False))
    environ.Env.read_env(str((environ.Path(__file__) - 2).path('video_analysis').path('.env')))

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    api_service_name = 'youtube'
    api_version = 'v3'
    DEVELOPER_KEY = env('YOUTUBE_API_KEY')

    client_secrets_file = env('GOOGLE_CLIENT_SECRET')

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.captions().list(
        part='snippet',
        videoId=yt_video_id
    )
    response = request.execute()

    caption_id = response['items'][0]['id']
    print('/************** {}'.format(caption_id))

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube2 = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request2 = youtube2.captions().download(
        id=caption_id
    )

    fh = io.FileIO(caption_id, 'wb')
    download = MediaIoBaseDownload(fh, request2)
    complete = False
    while not complete:
      status, complete = download.next_chunk()

    caption_file = open(caption_id,'r')
    print(caption_file.read())

    return response