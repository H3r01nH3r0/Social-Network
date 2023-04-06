import React, { useState } from "react";
import TextareaAutosize from 'react-textarea-autosize';


const PostUpdater = ({title, postText, onSubmit}) => {
    const [newTitle, setNewTitle] = useState(title)
    const [newPostText, setNewPostText] = useState(postText)

    const updatePost = () => {
        onSubmit(newTitle, newPostText)
    }

    return (
        <div className="post-updater">
            <h3>Update post content:</h3>
            <input
                placeholder="Update title..."
                value={newTitle}
                onChange={(e) => {setNewTitle(e.target.value)}}
            />
            <TextareaAutosize
                placeholder="Update post text..."
                value={newPostText}
                className="update-post-text"
                onChange={(e) => {setNewPostText(e.target.value)}}
            />
            <div className="update-media">
                <button onClick={updatePost}>Update</button>
            </div>
        </div>
    )
}

export default PostUpdater