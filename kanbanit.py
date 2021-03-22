import io
import os
# Imports the Google Cloud client library
from google.cloud import vision
import Functions
# Objeto de resposta do google não é serializável. 
# Converter para string perde os acentos
import json
import asyncio
# Dando esse erro: RepeatedComposite has no attribute DESCRIPTOR
# from google.protobuf.json_format import MessageToDict


def call_api(filepath, filename):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    name_only = filename.split('.')[0]

    # Loads the image into memory
    with io.open((filepath+'/'+filename), 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    # Saving the original response
    with open('Responses/Original/{}-soutput.txt'.format(name_only), 'w+', encoding='cp1252') as sOtp_file:
        sOtp_file.writelines(str(document))

    kanban_output = Functions.build_myjson(document)

    with open('Responses/Jsons/{}-joutput.json'.format(name_only), 'w+', encoding='cp1252', errors='ignore') as jOtp_file:
        json.dump(kanban_output, jOtp_file, ensure_ascii=False, indent=4)
    
    if response.error.message:
        raise Exception('{}\nFor more info on error messages, check: '
                        'https://cloud.google.com/apis/design/errors'.format(response.error.message))

def batch_call_api():
    file_dir = os.path.abspath('Images/')
    # every image in the directory is being processed by the api, resulting in jsons and text files in the correspondent folders
    for file_name in os.listdir(file_dir):
        call_api(file_dir, file_name)

def build_reports_batch():
    jsons_dir = os.path.abspath('Responses/Jsons/')
    
    for i_json_file in range(0, len(os.listdir(jsons_dir))):
        json_file = os.listdir(jsons_dir)[i_json_file]
        kanban = Functions.read_jkanban(jsons_dir + '/' + json_file)
        # Get kanban title without the joutput
        report_name = kanban.get_title().split('-joutput')[0]
        # Creates report file
        Functions.kanban_report(kanban, 'report-{}'.format(report_name))
        report_cont += 1

# "Batch call" to the images and files in the project
if __name__ == '__main__':
    # batch_call_api()
    # build_reports_batch()
    jsons_dir = os.path.abspath('Responses/Jsons/')
    
    kanban = Functions.read_jkanban(jsons_dir + '/' + 'Kanban-20-joutput.json')
    # Creates report file
    Functions.kanban_report(kanban, 'report-{}'.format('test'))