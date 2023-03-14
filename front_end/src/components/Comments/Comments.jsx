import "./comments.css"
import React, { useContext, useEffect, useState } from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import Divider from '@mui/material/Divider';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import instance from '../../utils/axios';
import AuthContext from "../../context/AuthContext";
import { extractUserId, extractHostId } from "../../utils/Token";
import MyRating from "../Drawer/MyRating";


export default function Comments(props) {

    const { token } = useContext(AuthContext);
    const user_id = extractUserId(token);
    const host_id = extractHostId(token);
    const a_id = props.a_id;

    const [message, setMessage] = useState("");
    const [rateValue, setrateValue] = useState(0);
    const [updateMessage, setUpdateMessage] = useState("");
    const [isReply, setIsReply] = useState(false);
    const [isEdit, setIsEdit] = useState(false);
    const [activeCommitId, setActiveCommitId] = useState(0);
    const [comments, setComments] = useState([]);


    // fetch all comments by activity id (a_id)
    useEffect(()=>{
        setTimeout(() => {
            getList();
        }, 100);
    }, [])

    const getList = () => {
        let params = { a_id: a_id };
        instance.post("/activities/commit/listall", params).then(res => {
            let data = res.data || [];
            setComments(data);
        })
    }

    // initialize the parameters for each method

    const values = {
        token: token,
        user_id: (user_id === null) ? '' : parseInt(user_id),
        host_id: (host_id === null) ? '' : parseInt(host_id),
        message: message,
        a_id: a_id,
    }

    const commit_params = {
        token: token,
        user_id: (user_id === null) ? '' : parseInt(user_id),
        host_id: (host_id === null) ? '' : parseInt(host_id),
        a_id: a_id,
        c_id: activeCommitId,
    }

    // the submit comment button
    const onSubmit = async (e) => {
        e.preventDefault();
        await instance.post('/activities/commit/add', {...values, rating: rateValue, message: message});
        getList();
        // after the action finished, set all state to the orignal state, clear the message, close the input text region
        setMessage('');
        setrateValue(0);
        setIsEdit(false);
        setIsReply(false);
        return false;
    };

    // the submit reply button
    const onReply = async (e) => {
        e.preventDefault();
        await instance.post('/activities/commit/reply', {...commit_params, message: updateMessage});
        getList();
        // after the action finished, set all state to the orignal state, clear the message, close the input text region
        setUpdateMessage('');
        setIsEdit(false);
        setIsReply(false);
        return false;
    };

    // the edit comment or reply button
    const onEdit = async (e) => {
        e.preventDefault();
        await instance.post('/activities/commit/edit', {...commit_params, message: updateMessage});
        getList();
        // after the action finished, set all state to the orignal state, clear the message, close the input text region
        setUpdateMessage('');
        setIsEdit(false);
        setIsReply(false);
        return false;
    };

    useEffect(()=>{
        setActiveCommitId(activeCommitId);
    },[activeCommitId])

    // the delete commit or reply button
    const onDelete = async (c_id) => {
        commit_params.c_id = c_id;
        await instance.post('/activities/commit/remove', {...commit_params});
        getList();
        setMessage("");
    };

    // the change rate (the stars that users give to the activity) button
    const onChangeRate = (newValue) => {
        let num;
        if (Number.isFinite(newValue)) {
            num = newValue * 2;
        } else {
            num = 0;
        }
        setrateValue(num)
    }

    return (
        <List sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper',margin:'0 auto' }}>
            {/* Show comment box with rating bar to user or only comment box to host by checking the existence of user id or host id */}
            { user_id ?
                (
                    <div className='form'>
                        <form onSubmit={onSubmit}>
                            <textarea
                                className="comment-form-textarea"
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                            />
                            <MyRating defaultValue={(rateValue / 2)} onChangeRate={onChangeRate}/>
                            <Button id='mbtn' variant="contained" size="medium" type='submit' color='secondary'>
                                Comment
                            </Button>
                        </form>
                    </div>
                ) : host_id ?
                (
                    <div className='form'>
                        <form onSubmit={onSubmit}>
                            <textarea
                                className="comment-form-textarea"
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                            />
                            <Button id='mbtn' variant="contained" size="medium" type='submit' color='secondary'>
                                Comment
                            </Button>
                        </form>
                    </div>
                ) : null
            }

            {/* use a map function to show all comments with the corresponsing reply by iteration */}
            { comments ? comments.map((item) => {
                // when it is a original comment, the number of reply is 0, otherwise it is a reply to a comment
                if (item.reply === 0) {
                    // get all replys by filtering the comment list by comparing the reply and commit id
                    const replys = comments.filter((comment) => comment.reply === item.commit_id)
                return (
                    <>
                        <ListItem alignItems="flex-start" key={item.commit_id}>
                            <ListItemAvatar>
                                <Avatar alt="Remy Sharp" src="/static/images/avatar/1.jpg" />
                            </ListItemAvatar>

                            <ListItemText
                                primary={item.sender_name}
                                secondary={
                                    <React.Fragment>
                                        <Typography
                                            sx={{ display: 'inline' }}
                                            component="span"
                                            variant="body2"
                                            color="text.primary"
                                        >
                                            {item.message}
                                            <br/>
                                        </Typography>
                                        Time: {item.time}
                                        <br/>
                                        Rating: <MyRating isdisabled={true} defaultValue={Number(item.rating)/2}/>
                                        <br/>
                                        {/* if the token is existed, then it is a user or host that already logged in, then show the reply, edit and delete button */}
                                        { token ? (
                                            <Box sx={{ '& button': { m: 1 } }}>
                                                <Button id='mbtn' variant="contained" size="small" color='secondary' onClick={() => {
                                                    setActiveCommitId(item.commit_id)
                                                    setIsReply(true)
                                                    setIsEdit(false)
                                                }}>
                                                    Reply
                                                </Button>
                                                <Button id='mbtn' variant="contained" size="small" color='secondary' onClick={() => {
                                                    setActiveCommitId(item.commit_id)
                                                    setIsEdit(true)
                                                    setIsReply(false)
                                                }}>
                                                    Edit
                                                </Button>
                                                <Button id='mbtn' variant="contained" size="small" color='secondary' onClick={() => {
                                                        onDelete(item.commit_id)
                                                    }}>
                                                        Delete
                                                    </Button>
                                                </Box>
                                            ) : null
                                        }
                                        {/* show the coresponding reply, edit input text box by checking the current actived commit id (which commit is currrently focused on) */}
                                        { isReply && !isEdit && item.commit_id === activeCommitId && (
                                            <div className='form'>
                                                <form onSubmit={onReply}>
                                                    <textarea
                                                        className="comment-form-textarea"
                                                        name='userReply'
                                                        value={updateMessage}
                                                        onChange={(e) => setUpdateMessage(e.target.value)}
                                                    />
                                                    <Box sx={{ '& button': { m: 1 } }}>
                                                        <Button id='mbtn' variant="contained" size="small" type='submit' color='secondary'>
                                                            Submit
                                                        </Button>
                                                        <Button id='mbtn' variant="contained" size="small" color='secondary' onClick={() => setIsReply(false)}>
                                                            Cancel
                                                        </Button>
                                                    </Box>
                                                </form>
                                            </div>
                                        )}
                                        { isEdit && !isReply && item.commit_id === activeCommitId && (
                                            <div className='form'>
                                                <form onSubmit={onEdit}>
                                                    <textarea
                                                        className="comment-form-textarea"
                                                        value={updateMessage}
                                                        name='userEdit'
                                                        onChange={(e) => setUpdateMessage(e.target.value)}
                                                    />
                                                    <Box sx={{ '& button': { m: 1 } }}>
                                                        <Button  id='mbtn'  variant="contained" size="small" type='submit' color='secondary'>
                                                            Submit
                                                        </Button>
                                                        <Button  id='mbtn' variant="contained" size="small" color='secondary' onClick={() => setIsEdit(false)}>
                                                            Cancel
                                                        </Button>
                                                    </Box>
                                                </form>
                                            </div>
                                        )}
                                    </React.Fragment>
                                    }
                                />
                            </ListItem>
                            {/* same logic showing the corresponding replys to each original comments */}
                            { replys.length !== 0 && replys.map((item) => {
                                return (
                                    <ListItem alignItems="flex-start" key={item.commit_id}>
                                        <ListItemAvatar>
                                            <Avatar alt="Remy Sharp" src="/static/images/avatar/1.jpg" />
                                        </ListItemAvatar>
                                        <ListItemText
                                            primary={item.sender_name}
                                            secondary={
                                                <React.Fragment>
                                                    <Typography
                                                        sx={{ display: 'inline' }}
                                                        component="span"
                                                        variant="body2"
                                                        color="text.primary"
                                                    >
                                                        {item.message}
                                                        <br/>
                                                    </Typography>
                                                    Time: {item.time}
                                                    <br/>
                                                    { token ? (
                                                        <Box sx={{ '& button': { m: 1 } }}>
                                                            <Button id='mbtn' variant="contained" size="small" color='secondary' onClick={() => {
                                                                setActiveCommitId(item.commit_id)
                                                                setIsEdit(true)
                                                                setIsReply(false)
                                                            }}>
                                                                Edit
                                                            </Button>
                                                            <Button  id='mbtn'  variant="contained" size="small" color='secondary' onClick={() => {
                                                                onDelete(item.commit_id)
                                                            }}>
                                                                Delete
                                                            </Button>
                                                        </Box>
                                                    ) : null
                                                    }
                                                    { isEdit && !isReply && item.commit_id === activeCommitId && (
                                                            <div className='form'>
                                                            <form onSubmit={onEdit}>
                                                                <textarea
                                                                    className="comment-form-textarea"
                                                                    value={updateMessage}
                                                                    name='userEdit'
                                                                    onChange={(e) => setUpdateMessage(e.target.value)}
                                                                />
                                                                <Box sx={{ '& button': { m: 1 } }}>
                                                                    <Button  id='mbtn'  variant="contained" size="small" type='submit' color='secondary'>
                                                                        Submit
                                                                    </Button>
                                                                    <Button  id='mbtn' variant="contained" size="small" color='secondary' onClick={() => setIsEdit(false)}>
                                                                        Cancel
                                                                    </Button>
                                                                </Box>
                                                            </form>
                                                        </div>
                                                    )}
                                                </React.Fragment>
                                            }
                                        />
                                    </ListItem>
                                )
                            })}
                        <Divider />
                    </>
                )
                } else {
                    return null
                }

            }) : <div></div>
            }
        </List>
    );
}