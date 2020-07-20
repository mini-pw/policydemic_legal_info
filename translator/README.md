#Translator

This module is responsible for translating text.
It uses IBM Watson Translator as translating service.

##API
There is one method in this module, called `translate`.
It takes one parameter as input: string containing text to tranlate.
It returns object of following structure:
```
    'translation_type': 'auto',
    'original_text': input_text,
    'translated_text': output_text,
    'language': language_name
```
If an error occurs there is also a field named `message` containing description of this error.

##Setting up IBM Watson Translator
This module requires Translator service running on IBM Cloud.
Instructions on how to setup an instance of this service can be found in IBM Cloud documentation:
***https://cloud.ibm.com/docs/language-translator?topic=language-translator-gettingstarted***

It is also required to supply credentials for the service, as described in ***https://pypi.org/project/ibm-watson/#authentication***
The "Credential file" method should be used.