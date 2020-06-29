import React, { useState } from 'react';
import SearchFormComponent from '../search/search-form.component.js';
import SearchResultsListComponent from '../search/search-results-list.component.js';
import { Container } from '@material-ui/core';
import NewDocDialogComponent from '../form/new-doc-dialog.component.js';
import NewDocFormComponent from '../form/new-doc-form.component.js';
import { useFormDialog } from '../../common/hooks/form-dialog-hook';
import EditDocDialogComponent from "../../components/form/edit-doc-dialog.component";

export default function SsdTabComponent() {
    const [openDialog, handleOpenDialog, handleCloseDialog] = useFormDialog();
    const [editedDocumentId, setEditedDocumentId] = useState();

    return (<Container>
        <SearchFormComponent />
        <NewDocDialogComponent open={openDialog} onClose={handleCloseDialog}>
            <NewDocFormComponent type="SSD" onSuccessfulSend={handleCloseDialog}/>
        </NewDocDialogComponent>
        {
            editedDocumentId && (
                <EditDocDialogComponent
                    open={true}
                    onClose={() => setEditedDocumentId(undefined)}
                    type="SSD"
                    onSuccess={() => setEditedDocumentId(undefined)}
                />
            )
        }
        <SearchResultsListComponent
            headerCaption="SSD"
            onAddNewItemClick={handleOpenDialog}
            onEdit={documentId => setEditedDocumentId(documentId)}
        />
    </Container>);
}