
import React from 'react';
import SearchFormComponent from '../search/search-form.component.js';
import SearchResultsListComponent from '../search/search-results-list.component'
import { Container } from '@material-ui/core';
import NewDocDialogComponent from '../form/new-doc-dialog.component.js';
import NewDocFormComponent from '../form/new-doc-form.component.js';
import { useFormDialog } from '../../common/hooks/form-dialog-hook';

export default function LadTabComponent() {
    const [openDialog, handleOpenDialog, handleCloseDialog] = useFormDialog();

    return (<Container>
        <SearchFormComponent />
        <NewDocDialogComponent open={openDialog} onClose={handleCloseDialog}>
            <NewDocFormComponent type="LAD" onSuccessfulSend={handleCloseDialog}/>
        </NewDocDialogComponent>
        <SearchResultsListComponent headerCaption="LAD" onAddNewItemClick={handleOpenDialog} />
    </Container>)

} 