from scheduler.celery import app
from ibm_watson import LanguageTranslatorV3
import requests
import json


@app.task
def translate_all():
    database_address = 'http://127.0.0.1:9200/'
    query = {
        "query": {
            "bool": {
                "must_not": [
                    {"match": {"language": "English"}},
                    {"exists": {"field": "translated_text"}}
                ]
            }
        }
    }
    headers = {'content-type': 'application/json'}
    counter = 0
    are_all_translated = True

    while True:
        # get documents for translation from elasticsearch
        response = requests.get(database_address + 'documents/_search', data=json.dumps(query), headers=headers)
        if response.status_code != 200:
            return {"message": "Couldn't retrieve documents from database.", "updated_documents_count": counter}
        ccl = response.content.decode('utf-8')
        parsed_response = json.loads(ccl)

        if parsed_response['hits']['total']['value'] == 0:
            break

        for document in parsed_response['hits']['hits']:
            text_to_translate = document['_source']['original_text']
            # translate text
            translation = translate(text_to_translate)
            if translation["translation_type"] == "missing":
                are_all_translated = False
                continue

            # update record in database
            update_query = {
                "script": {
                    "source": """
                        ctx._source.translation_type = params.type;
                        ctx._source.language = params.language;
                        ctx._source.translated_text = params.translated_text
                    """,
                    "lang": "painless",
                    "params": {
                        "type": translation["translation_type"],
                        "language": translation["language"],
                        "translated_text": translation["translated_text"]
                    }
                }
            }
            response = requests.post(database_address + 'documents/_update/' + document['_id'],
                                     data=json.dumps(update_query),
                                     headers=headers)

            if response.status_code == 200:
                counter += 1
            else:
                are_all_translated = False

    if are_all_translated:
        return {"message": "All documents have been translated.", "updated_documents_count": counter}
    else:
        return {"message": "Couldn't translate all of the documents.", "updated_documents_count": counter}


@app.task
def translate(text):
    BASE_LANGUAGE = 'en'
    LT_THRESH = 0.4
    LT_PAIRS = {
        'ar': 'Arabic',
        'bn': 'Bengali',
        'bg': 'Bulgarian',
        'zh': 'Chinese(Simplified)',
        'zh-TW': 'Chinese(Traditional)',
        'hr': 'Croatian',
        'cs': 'Czech',
        'da': 'Danish',
        'nl': 'Dutch',
        'en': 'English',
        'et': 'Estonian',
        'fi': 'Finnish',
        'fr': 'French',
        'de': 'German',
        'el': 'Greek',
        'gu': 'Gujarati',
        'he': 'Hebrew',
        'hi': 'Hindi',
        'hu': 'Hungarian',
        'ga': 'Irish',
        'id': 'Indonesian',
        'it': 'Italian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'lv': 'Latvian',
        'li': 'Lithuanian',
        'ms': 'Malay',
        'ml': 'Malayalam',
        'mt': 'Maltese',
        'ne': 'Nepali',
        'nb': 'Norwegian Bokmål',
        'pl': 'Polish',
        'pt': 'Portuguese',
        'ro': 'Romanian',
        'ru': 'Russian',
        'si': 'Sinhala',
        'sk': 'Slovak',
        'sl': 'Slovenian',
        'es': 'Spanish',
        'sv': 'Swedish',
        'ta': 'Tamil',
        'te': 'Telugu',
        'th': 'Thai',
        'tr': 'Turkish',
        'uk': 'Ukrainian',
        'ur': 'Urdu',
        'vi': 'Vietnamese'
    }

    # set up translator
    try:
        translator = LanguageTranslatorV3(
            version='2018-05-01'
        )
    except:
        return {
            'message': 'Please bind your language translator service',
            'translation_type': 'missing',
            'original_text': text,
            'translated_text': '',
            'language': ''
        }

    # detect language
    if text:
        response = translator.identify(text)
        res = response.get_result()
    else:
        res = None
    if res and res['languages'][0]['confidence'] > LT_THRESH:
        language = res['languages'][0]['language']
    elif res is None:
        language = BASE_LANGUAGE
    else:
        return {
            'message': 'Sorry, I am not able to detect the language you are speaking. Please try rephrasing.',
            'translation_type': 'missing',
            'original_text': text,
            'translated_text': '',
            'language': ''
        }

    # validate support for language
    if language not in LT_PAIRS.keys():
        return {
            'message': 'Sorry, I do not know how to translate between {} and {} yet.'.format(
                BASE_LANGUAGE, language
            ),
            'translation_type': 'missing',
            'original_text': text,
            'translated_text': '',
            'language': ''
        }

    # translate to base language if needed
    if language != BASE_LANGUAGE:
        response = translator.translate(
            text,
            source=language,
            target=BASE_LANGUAGE
        )
        res = response.get_result()
        output = res['translations'][0]['translation']
        language_name = LT_PAIRS[language]
        # print(output)
        return {
            'translation_type': 'auto',
            'original_text': text,
            'translated_text': output,
            'language': language_name
        }
    else:
        return {
            'translation_type': 'auto',
            'original_text': text,
            'translated_text': text,
            'language': LT_PAIRS[BASE_LANGUAGE]
        }

