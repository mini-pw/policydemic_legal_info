
import React from 'react';
import SearchFormComponent from '../search/search-form.component.js';
import SearchResultsListComponent from '../search/search-results-list.component.js';
import { Container } from '@material-ui/core';

export default class SsdTabComponent extends React.Component {
    render() {
        return (<Container>
            <SearchFormComponent/>
            <SearchResultsListComponent headerCaption="SSD"/>
        </Container>)
    }
}