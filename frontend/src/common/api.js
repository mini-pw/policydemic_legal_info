import axios from 'axios';

export default class Api {
    static baseUrl = "http://localhost:8000"

    static postDocument(type, data) {
        return this._postFormData(type.toLowerCase(), data)
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

    static getAutocompleteOptions(collectionName){
        return axios.get(`${this.baseUrl}/autocomplete/${collectionName}`);
    }
}