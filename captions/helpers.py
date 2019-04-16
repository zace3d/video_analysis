import io
import os
import json
import environ

import google_auth_oauthlib.flow
import googleapiclient.discovery
import google.oauth2.credentials

from googleapiclient import errors
from googleapiclient.http import MediaIoBaseDownload

from xml.dom import minidom

class NotFoundError(Exception):
    pass

scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']

def transcript(yt_video_id):
    try:
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

        # out_file = io.FileIO(caption_id, 'wb')
        out_file = io.BytesIO()
        download = MediaIoBaseDownload(out_file, request_download_caption)
        complete = False
        while not complete:
            status, complete = download.next_chunk()

        aux = {}
        captions = parse_ttml(out_file.getvalue())
        aux['results'] = captions
        result = json.dumps(aux)
    except errors.HttpError as e:
        if e.resp.status == 404:
            raise NotFoundError()
        raise 

    return result

##### Parse ttml file
def parse_ttml(value):
    dom = minidom.parseString(value)
    items = dom.getElementsByTagName('p')

    captions = []
    for elem in items:
        elem_value = iterate_child(elem, '')
        captions.append(elem_value)

    return ' '.join(captions)

###### Parse sbv file
def parse_sbv(file):
    captions = []
    with file as f:
        f.seek(0)
        for index, line in enumerate(f.readlines(), start=1):
            print('{}, {}'.format(index, line))
            if index % 2 == 0:
                captions.append(line.decode('utf-8'))
    return ' '.join(captions)

def iterate_child(node, text):
    if node.hasChildNodes():
        for subelem in node.childNodes:
            if subelem.nodeType == 3:
                text += subelem.nodeValue
            elif subelem.nodeType == 1:
                text += iterate_child(subelem, '')
    return text