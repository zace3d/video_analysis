import io
import os
import json
import environ

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google.oauth2.credentials

from googleapiclient.http import MediaIoBaseDownload

from xml.dom import minidom

scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']

def transcript(yt_video_id):
    env = environ.Env(DEBUG=(bool, False))
    environ.Env.read_env(str((environ.Path(__file__) - 2).path('video_analysis').path('.env')))

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    api_service_name = 'youtube'
    api_version = 'v3'

    yt_refresh_token = env('REFRESH_TOKEN')
    yt_client_id = env('CLIENT_ID')
    yt_client_secret = env('CLIENT_SECRET')

    # Get credentials and create an API client
    credentials = google.oauth2.credentials.Credentials(
        None,
        refresh_token=yt_refresh_token,
        client_id=yt_client_id,
        client_secret=yt_client_secret,
        scopes=scopes,
        token_uri='https://www.googleapis.com/oauth2/v4/token')

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request_captions_list = youtube.captions().list(
        part='snippet',
        videoId=yt_video_id
    )
    response = request_captions_list.execute()

    caption_id = response['items'][0]['id']
    # print('/**************Caption ID {}'.format(caption_id))

    #### Download Caption by ID
    request_download_caption = youtube.captions().download(
        id=caption_id,
        tfmt='ttml'
    )

    fh = io.FileIO(caption_id, 'wb')
    download = MediaIoBaseDownload(fh, request_download_caption)
    complete = False
    while not complete:
      status, complete = download.next_chunk()

    ##### Parse XML file
    dom = minidom.parse(caption_id)
    items = dom.getElementsByTagName('p')

    aux = {}
    captions = []
    for elem in items:
        elem_value = iterate_child(elem, '')
        captions.append(elem_value)

    aux['results'] = captions
    result = json.dumps(aux)

    return result

def iterate_child(node, text):
    if node.hasChildNodes():
        for subelem in node.childNodes:
            if subelem.nodeType == 3:
                text += subelem.nodeValue
            elif subelem.nodeType == 1:
                text += iterate_child(subelem, '')
    return text