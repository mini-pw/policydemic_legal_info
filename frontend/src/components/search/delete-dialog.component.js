import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

export default function DeleteConfirmationDialogComponent(props) {

  const { onDeleteExecute, onDeleteCancelExecute, dialogVisible } = props;

  const [ open, setOpen ] = React.useState(false);

  React.useEffect(() =>{
      setOpen(dialogVisible);
  }, [dialogVisible]);

  const handleClose = (dialogResult) => {

    if(dialogResult === true){
      onDeleteExecute();
    }
    else {
      onDeleteCancelExecute();
    }

    setOpen(false);
  };

  return (
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{"Delete records?"}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
              Selected records will be deleted from the database.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => handleClose(true)} color="primary" autoFocus>
            Yes
          </Button>
          <Button onClick={() => handleClose(false)} color="primary">
            No
          </Button>
        </DialogActions>
      </Dialog>
  );
}