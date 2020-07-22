#Translator

This module is responsible for translating text.
It uses IBM Watson Translator as translating service.

##API
###translate(text)
This method takes one parameter as input: string containing text to tranlate.
It returns a dictionary of following structure:
```
    'translation_type': 'auto',
    'original_text': input_text,
    'translated_text': output_text,
    'language': language_name
```
If an error occurs there is also a key named `message` containing description of this error.

###translate_all()
This method retrieves all documents that need to be translated from elasticsearch database 
(address of the database is set to "http://127.0.0.1:9200/"). Documents are searched by field `language` other than 
`English` and an empty `translated_text` field. Then it translates retrieved data using the `translate` method and updates
records in the database. It returns a dictionary: 
```
"message": "All documents have been translated.", 
"updated_documents_count": counter
```
`updated_documents_count` indicates how many documents were translated and then successfully updated, while `message` 
tells if everything went well. Message shown above is return in the best scenario, otherwise it can be one telling that
only some of the records were updated or that there is a problem with connection to the database.

##Setting up IBM Watson Translator
This module requires Translator service running on IBM Cloud.
Instructions on how to setup an instance of this service can be found in IBM Cloud documentation:
***https://cloud.ibm.com/docs/language-translator?topic=language-translator-gettingstarted***

It is also required to supply credentials for the service, as described in ***https://pypi.org/project/ibm-watson/#authentication***
The "Credential file" method should be used.

##Other possible translators
There are some other solutions for translating text. They differ between each other in usage, price and number of 
characters that can be translated for free each month. Here are links to some of them:

google: https://cloud.google.com/translate/

yandex: https://tech.yandex.com/translate/ 

microsoft: https://azure.microsoft.com/en-us/services/cognitive-services/translator/

systran: https://platform.systran.net/reference/translation/