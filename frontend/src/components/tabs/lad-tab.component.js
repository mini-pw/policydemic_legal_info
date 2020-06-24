
import React from 'react';
import SearchFormComponent from '../search/search-form.component.js';
import SearchResultsListComponent from '../search/search-results-list.component'
import { Container } from '@material-ui/core';

export default class LadTabComponent extends React.Component {
    render() {
        return (<Container>
            <SearchFormComponent/>
            <SearchResultsListComponent headerCaption="LAD"/>
        </Container>)
    }
} 