import React, { useState, useContext} from "react";
import { IoIosHeartEmpty, IoIosHeart, IoIosHammer, IoIosPerson } from 'react-icons/io';
import { BsTrashFill } from "react-icons/bs"
import DateTimeFormat from "../utils/DateFormater";
import {UserContext} from "../context/UserContext";
import PostUpdater from "./PostUpdater";

const baseURL = "http://127.0.0.1:8000"

const PostContainer = ({ content, onDelete }) => {
    const [token] = useContext(UserContext);
    const [title, setTitle] = useState(content.title)
    const [postText, setPostText] = useState(content.text)
    const [like_count, setLikeCount] = useState(content.like_count)
    const [isLiked, setIsLiked] = useState(content.is_liked)
    const [file] = useState(content.image_path)
    const [postUpdate, setPostUpdate] = useState(false)

    const submitPostLike = async () => {
        const requestOptions = {
            method: "PUT",
            headers: { 
                "Content-Type": "application/json",
                Authorization: "Bearer " + token,
            },
        }
        const response = await fetch(`${baseURL}/wall/like/${content.id}`, requestOptions)
        
        if (response.ok) {
            if (isLiked) {
                setLikeCount(like_count - 1)
            } else {
                setLikeCount(like_count + 1)
            }
            setIsLiked(!isLiked)
        }
    };

    const submitPostDelete = async () => {
        const requestOptions = {
            method: "DELETE",
            headers: { 
                "Content-Type": "application/json",
                Authorization: "Bearer " + token,
            },
        }
        const response = await fetch(`${baseURL}/wall/delete/${content.id}`, requestOptions)
        
        if (response.ok) {
            onDelete(content.id)
        }
    };

    const submitPostUpdate = async (newTitle, newText) => {
        const formdata = new FormData();
        formdata.append("title", newTitle)
        formdata.append("text", newText)
        const requestOptions = {
            method: "PATCH",
            headers: { 
                Authorization: "Bearer " + token,
            },
            body: formdata
        }
        const response = await fetch(`${baseURL}/wall/update/${content.id}`, requestOptions)
        const answer = await response.json()
        if (response.ok) {
            if (newTitle) {
                setTitle(newTitle)
            }
            if (newText) {
                setPostText(newText)
            }
        } else {
            console.log(answer)
        }
    };


    const likePost = () => {
        submitPostLike()
    }

    const deletePost = () => {
        submitPostDelete()
    }

    const updatePost = () => {
        setPostUpdate(!postUpdate)
    }

    const setNewValues = (newTitle, newText) => {
        setPostUpdate(!postUpdate)
        if (!(newTitle === title) && !(newText === postText)) {
            submitPostUpdate(newTitle, newText)
        }
    }

    return (
        <div className="post-container">
            <div className="post-header">
                <div className="user-profile">
                    <IoIosPerson className="default-user"/>
                    <span className="username">{ content.author.first_name } { content.author.last_name }</span>
                </div>
                <div className="post-date">
                    <DateTimeFormat datetimeString={content.publication_date}/>
                </div>
            </div>
            <div className="post-content">
                <div className="post-title">
                    <h1>{ title }</h1>
                </div>
                {content.image_path ? <img className="post-image" src={`data:image/png;base64,${file}`} alt="empty"/> : <></>}
                <div className="post-text">
                    <p>{ postText }</p>
                </div>
                <div className="post-reactions">
                    <div className="like">
                        {
                            !isLiked ? 
                            <IoIosHeartEmpty className="likeIcon" onClick={ likePost }/>:
                            <IoIosHeart className="likeIcon" onClick={ likePost }/>
                        }
                        <span className="like-count">{ like_count }</span>
                    </div>
                    {content.is_owner && 
                    <div className="update-remove">
                        <IoIosHammer className="update" onClick={ updatePost }/>
                        <BsTrashFill className="remove" onClick={ deletePost }/>
                    </div>}
                </div>
                {postUpdate && <PostUpdater title={title} postText={postText}  onSubmit={setNewValues}/>}
            </div>
        </div>
    )
}

export default PostContainer