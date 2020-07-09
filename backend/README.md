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

In order to run tests just use jest framework. All of the tests are placed in `index.test.js` file