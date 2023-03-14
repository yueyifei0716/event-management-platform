import React, { useState } from 'react';
// material-ui
import { Snackbar } from '@mui/material';
import MuiAlert from '@mui/material/Alert';

export default function Message(props) {
    const { content, duration, type } = {...props};
    // 开关控制：默认true,调用时会直接打开
    const [open, setOpen] = useState(true);
    // 关闭消息提示
    const handleClose = (event, reason) => {
        setOpen(false);
    };
    return (
        <Snackbar sx={{ width: '100%' }} spacing={2} open={open} autoHideDuration={duration} anchorOrigin={{ vertical: 'top', horizontal: 'center' }} onClose={handleClose}>
            <Alert severity={type} sx={{ width: '46%' }}>
                {/*  variant="standard" */}
                <div style={{fontSize:'12px'}} dangerouslySetInnerHTML={{__html:content}}>

                </div>
            </Alert>
        </Snackbar>
    );
}


const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});