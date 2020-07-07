
import React, { useEffect, useState } from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';
import Api from '../../common/api';
import NewDocFormComponent from "./new-doc-form.component";
import { CircularProgress } from '@material-ui/core';

export default function EditDocDialogComponent({ type, onSuccess, documentId, open, onClose, children }) {
    const [document, setDocument] = useState();    

    useEffect(() => {
        Api.getDocumentById()
            .then(response => setDocument(response.data));
    }, [documentId]);  

    return (
        <Dialog variant="outlined" fullScreen open={open} onClose={onClose} aria-labelledby="form-dialog-title">
            <DialogTitle id="form-dialog-title" onClose={onClose}>
                Edit document
            </DialogTitle>
            <DialogContent>
                {document
                    ? <NewDocFormComponent
                        type={type}
                        onSuccessfulSend={onSuccess}
                        document={document} />
                    : <CircularProgress />
                }
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="primary">
                    Cancel
                </Button>
                <Button form="edit-doc-form" type="submit" color="primary">
                    Save
                </Button>
            </DialogActions>
        </Dialog>
    )
} 