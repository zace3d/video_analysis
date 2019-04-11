# [START speech_quickstart]
import io
import tempfile
import json

# Imports the Google Cloud client library
# [START speech_python_migration_imports]
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from os import path

from ffmpy import FFmpeg
# [END speech_python_migration_imports]

def transcribe_file(speech_file):
    # Instantiates a client
    client = speech.SpeechClient()

    dirname = path.dirname(__file__)

    # Create video temp file
    tmp_video = tempfile.NamedTemporaryFile(suffix='.mp4')
    tmp_video.write(speech_file.read())

    # Create audio temp file
    tmp_audio_path = dirname + '/audios/' + path.splitext(speech_file.name)[0] + '.flac'

    # raise ValueError(tmp_audio_path)

    ### ffmpeg -i video.mp4 -vn -c:a flac audio.flac
    input_path = tmp_video.name
    output_path = tmp_audio_path
    ff = FFmpeg(
        inputs={input_path: None},
        outputs={output_path: '-vn -ac 1 -c:a flac -y'}
        )
    ff.cmd
    ff.run()
    # os.system("ffmpeg -i {0} -vn -c:a flac -y audio.flac".format(path_file))

    # Loads the audio into memory
    with io.open(output_path, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    # Recognition Config
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='es-MX',
        # Enhanced models are only available to projects that
        # opt in for audio data collection.
        use_enhanced=True,
        # A model must be specified to use enhanced model.
        model='default')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    alternatives = {}
    for result in response.results:
        alternatives['transcript'] = '{}'.format(result.alternatives[0].transcript)
        alternatives['confidence'] = '{}'.format(result.alternatives[0].confidence)

        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))
    
    results = {}
    results['alternatives'] = alternatives

    tmp_video.close()

    print('***************************')
    print(json.dumps(results))
    print('***************************')

    return json.dumps(results)
    # [END speech_quickstart]