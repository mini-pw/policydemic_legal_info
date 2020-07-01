
import React from 'react';
import SearchFormComponent from '../search/search-form.component.js';
import SearchResultsListComponent from '../search/search-results-list.component.js';
import { Container } from '@material-ui/core';
import NewDocDialogComponent from '../form/new-doc-dialog.component.js';
import NewDocFormComponent from '../form/new-doc-form.component.js';
import { useFormDialog } from '../../common/hooks/form-dialog-hook';

export default function SsdTabComponent() {
    const [openDialog, handleOpenDialog, handleCloseDialog] = useFormDialog();

    return (<Container>
        <SearchFormComponent />
        <NewDocDialogComponent open={openDialog} onClose={handleCloseDialog}>
            <NewDocFormComponent type="SSD" onSuccessfulSend={handleCloseDialog}/>
        </NewDocDialogComponent>
        <SearchResultsListComponent headerCaption="SSD" onAddNewItemClick={handleOpenDialog}/>
    </Container>);
}