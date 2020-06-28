
import React from 'react';
import SearchFormComponent from '../search/search-form.component.js';
import SearchResultsListComponent from '../search/search-results-list.component.js';
import { Container } from '@material-ui/core';
import NewDocDialogComponent from '../form/new-doc-dialog.component.js';
import NewDocFormComponent from '../form/new-doc-form.component.js';
import { useFormDialog } from '../../common/hooks/form-dialog-hook';

import Api from '../../common/api.js';

export default function SsdTabComponent() {

    const [openDialog, handleOpenDialog, handleCloseDialog] = useFormDialog();

    const [searchResults, setSearchResults] = React.useState([]);

    const handleSearch = (formData) => {

        Api.getSearchResults("SSD", formData).then((resp) => 
        {
            setSearchResults(resp);
        });
    }

    const handleReset = () => {
        setSearchResults([]);
    }

    const handleOnDelete = (selected) => {
        alert(selected.join(','));
    }

    return (<Container>
        <SearchFormComponent onSearch={handleSearch} onReset={handleReset}/>
        <NewDocDialogComponent open={openDialog} onClose={handleCloseDialog}>
            <NewDocFormComponent type="SSD" onSuccessfulSend={handleCloseDialog}/>
        </NewDocDialogComponent>
        <SearchResultsListComponent headerCaption="SSD" onAddNewItemClick={handleOpenDialog} searchResultsList={searchResults} onDelete={handleOnDelete}/>
    </Container>);
}