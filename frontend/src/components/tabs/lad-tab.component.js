
import React from 'react';
import SearchFormComponent from '../search/search-form.component.js';
import SearchResultsListComponent from '../search/search-results-list.component'

export default class LadTabComponent extends React.Component {
    render() {
        return (<div>
            <SearchFormComponent/>
            <SearchResultsListComponent headerCaption="LAD"/>
        </div>)
    }
} 