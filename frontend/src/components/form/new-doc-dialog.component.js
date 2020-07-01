
import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';

export default function NewDocDialogComponent({ open, onClose, children }) {
    return (
        <Dialog variant="outlined" fullScreen open={open} onClose={onClose} aria-labelledby="form-dialog-title">
            <DialogTitle id="form-dialog-title" onClose={onClose}>
                Add Document
            </DialogTitle>
            <DialogContent>
                {children}
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="primary">
                    Cancel
                </Button>
                <Button form="new-doc-form" type="submit" color="primary">
                    Save
                </Button>
            </DialogActions>
        </Dialog>
    )
} 