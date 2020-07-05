from scheduler.celery import app
from ibm_watson import LanguageTranslatorV3


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
