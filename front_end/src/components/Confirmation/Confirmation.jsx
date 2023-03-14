import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogActions from '@material-ui/core/DialogActions';
import Dialog from '@material-ui/core/Dialog';

const useStyles = makeStyles((theme) => ({
    root: {
      width: '100%',
      maxWidth: 360,
      backgroundColor: theme.palette.background.paper,
    },
    paper: {
      width: '80%',
      maxHeight: 435,
      background: 'linear-gradient(190deg, #cddaf3 0%, #be9bd2 85%)',
      backgroundRepeat: 'no-repeat',
      backgroundSize: 'cover',
    //   height: 100vh;
    },
  }));

export default function ConfirmationDialogRaw(props) {
  const classes = useStyles();
  const { onClose, open, title,content,children,contentStyle,isBackBtn = true, ...other } = props;

  const handleCancel = () => {
    onClose && onClose();
  };

  const handleOk = () => {
    onClose && onClose(true);
  };


  return (
    <Dialog
      maxWidth="xs"
      aria-labelledby="confirmation-dialog-title"
      open={open || false}
      classes={{
        paper: classes.paper,
      }}
      {...other}
    >
      <DialogTitle id="confirmation-dialog-title">{title || '标题'}</DialogTitle>
      <DialogContent dividers style={contentStyle}>
       {content}
       {children}
      </DialogContent>
      <DialogActions>
        {isBackBtn && <Button variant="contained" autoFocus onClick={handleCancel} color="primary">
          Back
        </Button>}
        <Button variant="contained" onClick={handleOk} color="primary">
          Ok
        </Button>
      </DialogActions>
    </Dialog>
  );
}
