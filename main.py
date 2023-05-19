# pip install openai
# pip install moviepy
import os
import openai
from moviepy.editor import AudioFileClip
from math import *

# pip install requests
# pip install sseclient-py
import requests
import sseclient
import json

os.environ["OPENAI_API_KEY"] = "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"
# openai.organization = "org-o8OjIggTayep6O8WOBvnKG0P" // A CREER
openai.api_key = os.getenv("OPENAI_API_KEY")

# audio to text
def transcriptionFile(nameFile):
    audio_file_path = os.path.join(os.getcwd(), nameFile)

    audio_file = open(audio_file_path, "rb")
    transcript = openai.Audio.transcribe(
        file=audio_file,
        model="whisper-1",
        response_format='text',
        prompt=(
            'Can you make the transcription of the video?'
        )
    )

    return transcript


# cut audio
def cutAudioFile(masterAudioFile):
    audio_file_path = os.path.join(os.getcwd(), masterAudioFile)
    input_audio_clip = AudioFileClip(audio_file_path)
    input_audio_clip_duree = input_audio_clip.duration #total seconde
    tempMax = 25 * 60

    finaltranscription = ""
    if input_audio_clip_duree > tempMax:
        nbrTempFileAudio = ceil(input_audio_clip_duree / tempMax)

        startTime = 0
        EndTime = tempMax
        try:
            for i in range(0, nbrTempFileAudio):
                if i == (nbrTempFileAudio - 1):
                    EndTime = input_audio_clip_duree
                final_clip = input_audio_clip.subclip(startTime, EndTime)   #cut de l'audio start seconde, end seconde
                aNameAudioFile = "output" + str(i) + ".mp3"
                final_clip.write_audiofile(aNameAudioFile)                  #New audio file
                aTranscription = transcriptionFile(aNameAudioFile)          #retranscription du fichier audio
                finaltranscription = finaltranscription + aTranscription    #retranscription totale
                os.remove(aNameAudioFile)                                   #delete file audio
                startTime = EndTime
                EndTime = EndTime + tempMax

        except:
            print("error division video dans un LOG")

    f = open(masterAudioFile + ".txt", "a", encoding="utf-8")                 #creation du fichier texte
    f.write(finaltranscription)                                        #ecriture dans le fichier texte
    f.close()
    # #fichiers .txt peuvent contenir max 4000 mots
    # countWordInFinalTranscription = len(finaltranscription.split())
    # maxTokenGPT3 = 4000
    # nbrTextFile = ceil(countWordInFinalTranscription / maxTokenGPT3)
    # start = 0
    # end = maxTokenGPT3 - 1
    # for i in range(0, nbrTextFile):
    #     f = open(masterAudioFile + "-" + str(i) + ".txt", "a")              #creation du fichier texte
    #     f.write(finaltranscription[start:end])                              #ecriture dans le fichier texte
    #     f.close()
    #     start = end + 1
    #     end = end + maxTokenGPT3


# cutAudioFile("video90min.mp3")

#######
# resume a partir URL
# def create_summary_from_url(url):
#     prompt = f"Donne moi 30 mots cles sur le contenu de la page à l'URL suivante : {url}. Soit sur a plus de 80% pour ta réponse."

#     # Appel à l'API OpenAI pour générer un résumé
#     response = openai.Completion.create(
#         engine='text-davinci-003',
#         prompt=prompt,
#         max_tokens=500,
#         temperature=0.3,
#         n=1,
#         stop=None,
#     )

#     summary = response.choices[0].text.strip()
#     return summary

# # Exemple d'utilisation
# url = "https://sapimaux.com/blogs/infos/test"  # Remplacez par l'URL de votre choix
# summary = create_summary_from_url(url)
# print(summary)

import requests

url = "https://sapimaux.com/blogs/infos/test"
response = requests.get(url)
transcript = response.text

print(transcript)






#CHATGPT####################
# Message
# reqURL = "https://api.openai.com/v1/engines/davinci/completions"
# reqHeaders = {
#     "Accept" : "application/json",
#     "Authorization": "Bearer " + openai.api_key
# }

# reqBody = {
#     "prompt": "What is python? ",
#     "max_tokens": 100,
#     "temperature": 0,
#     "stream": True,
# }
# request = requests.post(reqURL, headers=reqHeaders, json=reqBody)
# client = sseclient.SSEClient(request)
# for event in client.events():
#     if event.data != "[DONE]":
#         print(json.loads(event.data)["choices"][0]["text"])
#     else:
#         break

##############
# messages = [
#     {"role": "system", "content": "Donne moi la 1ere phrase du fichier Texte"},
# ]

# chat = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo", messages=messages
# )
    
# reply = chat.choices[0].message.content
# print(f"ChatGPT: {reply}")
# messages.append({"role": "assistant", "content": reply})


######
# def upload_file(file_path):
#     with open(file_path, 'rb') as file:
#         response = openai.File.create(file=file, purpose='fine-tune')
#         return response['id']

# # Exemple d'utilisation
# file_path = os.path.join(os.getcwd(), "fulltext.json")
# file_id = upload_file(file_path)
# print(f"Le fichier a été téléchargé avec succès. ID du fichier : {file_id}")
