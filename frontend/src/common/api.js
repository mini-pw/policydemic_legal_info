import axios from 'axios';

export default class Api {
    static baseUrl = "http://localhost:8000"

    static postDocument(type, data) {
        return this._postFormData(type.toLowerCase(), data);
    }

    static createDataForRow(id, source, infoDate, language, keywords, country) {
        return {
            id: id,
            source: source,
            infoDate: infoDate,
            language: language,
            keywords: keywords,
            country: country
        };
    }

    static getSearchResults(type, data) {

        var rows = [
            Api.createDataForRow(1, "International Labour Organization", new Date(1995, 4, 4), "english", "cinemas", "Canada"),
            Api.createDataForRow(2, "Coronavirus Government Response Tracker", new Date(1998, 0, 14), "french", "pubs", "Italy"),
            Api.createDataForRow(3, "Coronavirus Government Response Tracker", new Date(1990, 3, 24), "french", "pubs", "Italy")
        ];

        return new Promise((resolve, reject) => {
            setTimeout(resolve, 100, rows);
        });

        //return this._postFormData(type.toLowerCase() + '/search', data);
    }

    static _postFormData(relativeUrl, data) {
        var formData = new FormData();
        Object.keys(data).forEach(key => formData.append(key, data[key]));

        return axios.post(`${this.baseUrl}/${relativeUrl}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
    }

    static getAutocompleteOptions(collectionName) {
        return axios.get(`${this.baseUrl}/autocomplete/${collectionName}`);
    }
}