# Nodejs Backend

## Running the server
In order to run a server, run following command
```bash
yarn run start 
````

## Endpoints

### Populating ElasticSearch
In order to populate ElasticSearch just call endpoint `localhost:8000/populate`
### Searching for documents
API provides two endpoints, for searching for legal acts and secondary source documents. The body of a rquest should look as follows

```json
{
	"web_page":["test_webpage.com", "test_webpageDE.com"],
	"country": ["Poland", "Germany"],
	"language": ["Polish", "German", "Italian"],
	"keywords":["keyword1", "keyword2"],
	"infoDateFrom": "2020-01-01",
	"infoDateTo": "2021-01-01"
}
``` 

### Searching for legal act documents

In order to look for legal acts documents one should make POST request to the endpoint `localhost:8000/lad/search` with proper request body defined above

### Searching for secondary documents

In order to look for secondary sources documents one should make POST request to the endpoint `localhost:8000/ssd/search` with proper request body defined above

### Response JSON

Response from server has following structure

```json
    {
        "id": "eyTWKHMBXm-PJsPs7XdC",
        "infoDate": "2020-12-15",
        "language": "Polish",
        "keywords": [
            "polska",
            "covid",
            "pandemia"
        ],
        "country": "Poland",
        "source": "Ministerstwo Zdrowia"
    }
```

### Tests

In order to run tests just run `yarn test` inside this directory.


### Further development

In order to receive more data, one just need to edit function `parseData`. The received object from elastic looks as follows 

```json
            {
                "_index": "documents",
                "_type": "_doc",
                "_id": "2RSKNHMBV-g9zj7jA9CQ",
                "_score": 1,
                "_source": {
                    "web_page": "test_webpage.gov.pl",
                    "document_type": "secondary",
                    "pdf_path": "test_path",
                    "scrap_date": "2020-10-05 10:00:00",
                    "info_date": "2020-12-15",
                    "country": "Poland",
                    "language": "Polish",
                    "translation_type": "automatic",
                    "text_parsing_type": "ocr",
                    "keywords": [
                        "poland",
                        "covid",
                        "pandemia"
                    ],
                    "original_text": "Oryginalny tekst dokumentu",
                    "translated_text": "Original text of the document",
                    "organization": "Test2",
                    "section": null
                }
```

and it is parsed by function `parseData` mentioned above to following form required by frontend TableView

```javascript
function parseData(data){
    const parsedData = [];
    data.forEach(element => {
        parsedData.push({
            id: element._id,
            source: element._source.organization,
            infoDate: element._source.info_date,
            language: element._source.language,
            keywords: element._source.keywords,
            country: element._source.country
        })
    });
    return parsedData;
}
```

### Setup local instance of ElasticSearch

To setup local instance of ElasticSearch just execute this command

```bash
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.8.0
```
Elastic will be available under `localhost:9200`