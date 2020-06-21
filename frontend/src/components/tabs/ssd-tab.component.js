
import React from 'react';
import SearchFormComponent from '../search/search-form.component.js';
import SearchResultsListComponent from '../search/search-results-list.component.js';

export default class SsdTabComponent extends React.Component {
    render() {
        return (<div>
            <SearchFormComponent/>
            <SearchResultsListComponent headerCaption="SSD"/>
        </div>)
    }
}