# from courses.models import LessonVideo
# # from helpers.embeddings import generate_transcript
# from celery import shared_task
# import moviepy as mp
# import speech_recognition as sr

# @shared_task
# def generate_transcript_task(video_id):
#     """
#     Task to generate a transcript using T5 summarization.
#     """
#     try:
#         # Get the video instance
#         video = LessonVideo.objects.get(id=video_id)

#         # Extract audio from video
#         video_path = video.video.url
#         audio_path = video_path.replace('.mp4', '.wav')

#         # Extract audio using moviepy
#         clip = mp.VideoFileClip(video_path)
#         clip.audio.write_audiofile(audio_path)

#         # Convert audio to text using SpeechRecognition
#         recognizer = sr.Recognizer()
#         with sr.AudioFile(audio_path) as source:
#             audio = recognizer.record(source)
#             raw_text = recognizer.recognize_google_cloud(audio)  # Convert audio to text

#         # Generate the summarized transcript using T5
#         summarized_transcript = generate_transcript(raw_text)
#         print(summarized_transcript)
#         # Save the transcript in the database
#         video.transcript = summarized_transcript
#         video.save()

#     except Exception as e:
#         print(f"Error in generate_transcript_task: {e}")
#         raise