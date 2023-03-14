import React, { useState, useEffect, useContext } from 'react'
import instance from '../../utils/axios';
import Drawer from '@material-ui/core/Drawer';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Divider from '@material-ui/core/Divider';
import Paper from '@material-ui/core/Paper';
import CloseIcon from '@material-ui/icons/Close';
import Badge from '@material-ui/core/Badge';
import { makeStyles } from '@material-ui/core/styles';
import { extractUserId } from "../../utils/Token";
import AuthContext from "../../context/AuthContext";
import IconButton from '@material-ui/core/IconButton';


const useStyles = makeStyles((theme) => ({
  root: {
    padding: '10px',
    overflow: 'auto',
  },
  card: {
    minWidth: 275,
    height: '160px',
    overflow: 'hidden',
    padding: '15px',
    margin: '15px'
  },
  paper: {
    padding: theme.spacing(2),

  },
}));


export default function Notic(props) {
  const classes = useStyles();
  const [dataList, setdataList] = useState([])

  const { isOpen, closeFun, changeNum } = props
  const { token } = useContext(AuthContext);
  const user_id = extractUserId(token);

  useEffect(() => {

    // setTimeout(() => {
    getList()
    // }, 200);
  }, [])
  const getList = () => {
    // wait(1000);
    let params = {
      user_id: user_id,
      token: token
    }
    console.log(11, params);
    //if(!sessionStorage.getItem('noticFlag')){
    instance.post(`/user/allnotifications`, params).then(res => {
      console.log(res.data, 'res--');
      //sessionStorage.setItem('noticFlag',true)
      let data = res.data.notifications || []
      setdataList(data)
      let num = res.data.unread_notifications
      changeNum(num)
    })
    //}
  }
  //   卡片点击事件
  const cardClick = v => {
    console.log(v)
    let data = {
      user_id: user_id,
      token: token,
      notification_id: v.id
    }
    instance.post(`/user/unreadnotifications`, data).then(res => {
      console.log(res, 222);
      getList()
    })

  }
  //   卡片关闭icon 事件
  const cardClose = (e, v) => {
    e.stopPropagation()
    console.log(v)
    let data = {
      user_id: user_id,
      token: token,
      notification_id: v.id
    }
    instance.post(`/user/deletenotification`, data).then(res => {
      console.log(res, 222);
      getList()
    })
  }

  return (
    <div className='myNoti'>
      <Drawer className={classes.root} anchor={'right'} open={isOpen} onClose={closeFun}>
        <div style={{ overflow: 'auto', height: '100%' }}>

          <Paper className={classes.paper}> Notification
            <IconButton id="close" onClick={closeFun} style={{ float: 'right', padding: '0px' }} name="closeNoti">
              <CloseIcon />
            </IconButton>
          </Paper>
          <Divider />
          {dataList.length ? dataList.map((v, i) => {
            return <Card className={classes.card} key={i} onClick={() => cardClick(v)}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Badge color={v.is_read === 1 ? "secondary" : 'primary'} overlap='circular' badgeContent="" variant="dot" />
                <CloseIcon style={{ cursor: 'pointer' }} onClick={(e) => cardClose(e, v)} />
              </div>
              <CardContent>
                <div> {v.message}  </div>


              </CardContent>
              <div style={{ textAlign: 'right' }}>{v.time}</div>
            </Card>
          }) : <div style={{ width: '275px' }}></div>}
        </div>
      </Drawer>
    </div>
  )
}
