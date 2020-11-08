
import sys

def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""


    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="en-US",
        audio_channel_count=2,
        model="video",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
        use_enhanced=True,
        diarization_config=speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=True,
            min_speaker_count=4,
            max_speaker_count=6,
        )
        
    )

    operation = client.long_running_recognize(
        request={"config": config, "audio": audio}
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=1000)

    
    with open('output.txt', 'w') as f:
        print(response, file=f)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))


    speaker_tags = response.results[-1]
    with open('speakers.txt', 'w') as f:
        curr_speaker = 0
        prev_speaker = speaker_tags.alternatives[0].words[0].speaker_tag
        curr_block = ""
        blocks = []
        for words in speaker_tags.alternatives[0].words:
            curr_speaker = words.speaker_tag
            if curr_speaker != prev_speaker:
                print('suh')
                
                blocks.append(curr_block)
                print("\n" + str(prev_speaker), file=f)
                prev_speaker = curr_speaker
                print(curr_block, file=f)
                curr_block = ""
            curr_block = curr_block + " " + words.word
        print("\n" + str(curr_speaker), file=f)
        print(curr_block, file=f)

        
                





transcribe_gcs("gs://kt38/trimmed-daily-2.flac")