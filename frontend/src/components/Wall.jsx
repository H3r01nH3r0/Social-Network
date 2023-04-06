import React, { useState, useContext, useEffect } from "react";
import {UserContext} from "../context/UserContext";
import Menu from "./Menu";
import PostContainer from "./PostContainer";
import EnterPost from "./EnterPost";
import { IoIosAddCircleOutline }from 'react-icons/io';



const baseURL = "http://127.0.0.1:8000"

const Wall = () => {
    
    const [token] = useContext(UserContext);
    const [postList, setPostList] = useState([]);
    const [createWindow, setCreateWindow] = useState(false)
    const [clicked, setClicked] = useState(false);

    const getPosts = async () => {
        const requestOptions = {
            method: "GET",
            headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
            },
        };
        const response = await fetch(`${baseURL}/wall/`, requestOptions);
        const data = await response.json()
        if (response.ok) {
            setPostList(data)
        }
    }


    useEffect(() => {
        getPosts();
    }, []);

    const createPost = () => {
        setClicked(!clicked);
        setCreateWindow(!createWindow)
    }

    const addPostToPostList = (newPost) => {
        setClicked(!clicked);
        setPostList([newPost, ...postList])
        setCreateWindow(false)

    }

    const onDeletePost = (id) => {
        setPostList(postList.filter((el) => el.id !== id))
    }

    return (
        <div className="wall-container">
            <Menu />
            <div className="content">
                {createWindow ? <EnterPost onSuccess={ addPostToPostList }/> : <></>}
                <div className="posts-container">
                    {postList.length > 0 ? postList.map(post => (
                        <PostContainer key={post.id} content={post} onDelete={ onDeletePost }/>
                    )) : <div className="no-content">
                            <h3>Create the first post!</h3>
                            <p>There's nothing here yet, but you can fix it!</p>
                        </div>}
                </div>
            </div>
            <div className="create-container">
                <div className={`create-btn${clicked ? ' clicked' : ''}`} onClick={createPost}>
                    <IoIosAddCircleOutline className={`create-icon${clicked ? ' rotated' : ''}`}/>
                </div>
            </div>
        </div>
    )
}

export default Wall