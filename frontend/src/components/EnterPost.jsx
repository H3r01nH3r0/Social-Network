import React, { useState, useRef, useContext } from "react";
import {AiOutlinePaperClip} from "react-icons/ai";
import { BsTrashFill } from "react-icons/bs"
import TextareaAutosize from 'react-textarea-autosize';
import {UserContext} from "../context/UserContext";

const baseURL = "http://127.0.0.1:8000"

const EnterPost = ({ onSuccess }) => {
    const [title, setTitle] = useState("")
    const [postText, setPostText] = useState("")
    const [file, setFile] = useState("")
    const [token] = useContext(UserContext);
    const fileInputRef = useRef(null);

    const CreatePost = async () => {
        const formData = new FormData();
        formData.append("title", title)
        formData.append("text", postText)
        formData.append("file", file)
        const requestOptions = {
            method: "POST",
            headers: {
              Authorization: "Bearer " + token,
            },
            body: formData
        };
        const response = await fetch(`${baseURL}/wall/create`, requestOptions)
        const answer =  await response.json()
        if (response.ok) {
            onSuccess(answer);
        }
    }
    

    const handleFileInputChange = (event) => {
      setFile(event.target.files[0]);
    };
    
    const handleAddMediaClick = () => {
      fileInputRef.current.click();
    };

    const deletePicture = () => {
        setFile("")
    }

    const sendData = () => {
        CreatePost()
    }
    
    return (
        <div className="create-post">
            <input
                type="text"
                placeholder="Title"
                maxLength="100"
                value={title}
                onChange={(e) => {setTitle(e.target.value)}}
                required
            />
            <TextareaAutosize
                type="text"
                className="enter-post-text" 
                maxLength="500"
                value={postText}
                placeholder="Enter your post text here..."
                onChange={(e) => {setPostText(e.target.value)}}
                required
            />
            {file && (
                <img
                    src={URL.createObjectURL(file)}
                    alt="uploaded image"
                />
            )}
            <div className="add-media">
                <div className="icons">
                {!file && <AiOutlinePaperClip
                    className="add-media-icon"
                    onClick={handleAddMediaClick}
                />}
                {file && <BsTrashFill 
                    className="delete-media-icon"
                    onClick={deletePicture}
                />}
                <input
                    type="file"
                    ref={fileInputRef}
                    style={{ display: "none" }}
                    onChange={handleFileInputChange}
                />
                </div>
                <button onClick={sendData}>Create</button>
            </div>
        </div>
    )
}

export default EnterPost