
describe('Creation of queries tests', function () {

    const constructParams = require('./index')

    it('When no data provided in request body query consist only of date and document type', function () {

        let bodyRequest = {
            "web_page":[],
            "country": [],
            "language": [],
            "keywords":[],
            "infoDateFrom": "2020-01-01",
            "infoDateTo": "2021-01-01"
        };

        let expectedQuery = {
            "index": "documents",
            "body": {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"document_type": "legalact"}},
                            {"range": {"info_date": {"gte": "2020-01-01", "lte": "2021-01-01"}}}
                        ]
                    }
                }
            }
        };

        let result = constructParams(bodyRequest,'legalact');

        expect(result).toStrictEqual(expectedQuery);

    });

    it('When one of each parameters is provided query contains one value for every key', function () {

        let bodyRequest = {
            "web_page":["test_webpage.com"],
            "country": ["Poland"],
            "language": ["Polish"],
            "keywords":["keyword"],
            "infoDateFrom": "2020-01-01",
            "infoDateTo": "2021-01-01"
        };

        let expectedQuery = {
            "index": "documents",
            "body": {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"document_type": "legalact"}},
                            {"range": {"info_date": {"gte": "2020-01-01", "lte": "2021-01-01"}}},
                            { "bool":{"should": [{"match":{"web_page" : "test_webpage.com" } }]}},
                            { "bool":{"should": [{"match":{"country" : "Poland" } }]}},
                            { "bool":{"should": [{"match":{"language" : "Polish" } }]}},
                            { "bool":{"should": [{"match":{"keywords" : "keyword" } }]}}
                        ]
                    }
                }
            }
        };

        let result = constructParams(bodyRequest,'legalact');

        expect(result).toStrictEqual(expectedQuery);

    });

    it('When multiple values are passed for one of the parameters query should have multiple match queries enclosed in should clause', function () {
        let bodyRequest = {
            "web_page": ["test_webpage.com", "test_webpage23.com"],
            "country": ["Poland"],
            "language": ["Polish"],
            "keywords": ["keyword"],
            "infoDateFrom": "2020-01-01",
            "infoDateTo": "2021-01-01"
        };

        let expectedQuery = {
            "index": "documents",
            "body": {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"document_type": "legalact"}},
                            {"range": {"info_date": {"gte": "2020-01-01", "lte": "2021-01-01"}}},
                            {"bool": {"should": [{"match": {"web_page": "test_webpage.com"}}, {"match": {"web_page": "test_webpage23.com"}}]}},
                            {"bool": {"should": [{"match": {"country": "Poland"}}]}},
                            {"bool": {"should": [{"match": {"language": "Polish"}}]}},
                            {"bool": {"should": [{"match": {"keywords": "keyword"}}]}}
                        ]
                    }
                }
            }
        };

        let result = constructParams(bodyRequest, 'legalact');

        expect(result).toStrictEqual(expectedQuery);

    });

    it('When multiple values are passed for multiple of the parameters query should have multiple match queries enclosed in should clause', function () {
        let bodyRequest = {
            "web_page": ["test_webpage.com", "test_webpage23.com"],
            "country": ["Poland", "Germany"],
            "language": ["Polish"],
            "keywords": ["keyword"],
            "infoDateFrom": "2020-01-01",
            "infoDateTo": "2021-01-01"
        };

        let expectedQuery = {
            "index": "documents",
            "body": {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"document_type": "legalact"}},
                            {"range": {"info_date": {"gte": "2020-01-01", "lte": "2021-01-01"}}},
                            {"bool": {"should": [{"match": {"web_page": "test_webpage.com"}}, {"match": {"web_page": "test_webpage23.com"}}]}},
                            {"bool": {"should": [{"match": {"country": "Poland"}}, {"match": {"country": "Germany"}}]}},
                            {"bool": {"should": [{"match": {"language": "Polish"}}]}},
                            {"bool": {"should": [{"match": {"keywords": "keyword"}}]}}
                        ]
                    }
                }
            }
        };

        let result = constructParams(bodyRequest, 'legalact');

        expect(result).toStrictEqual(expectedQuery);

    });

    it('When secondary document type is provided query will look for secondary document type', function () {

        let bodyRequest = {
            "web_page":[],
            "country": [],
            "language": [],
            "keywords":[],
            "infoDateFrom": "",
            "infoDateTo": ""
        };

        let expectedQuery = {
            "index": "documents",
            "body": {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"document_type": "secondary"}}
                        ]
                    }
                }
            }
        };

        let result = constructParams(bodyRequest, "secondary")

        expect(result).toStrictEqual(expectedQuery)
    })
})