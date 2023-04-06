import React, {useState} from "react";
import { IoIosSearch } from "react-icons/io"

const Header = () => {
    const [search, setSearch] = useState("");
    const onKeyDown = () => {
        console.log(search)
    } 
    return (
        <header className="header">
            <div className="sub-header">
                <div className="logo-header">
                    <h1>My<span className="color-text">Site</span></h1>
                </div>
                {/* <div className="search">
                    <input
                        type="text"
                        placeholder="Search..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        onKeyDown={onKeyDown}
                    />
                    <IoIosSearch className="search-icon"/>
                </div> */}
            </div>
        </header>
    )
}

export default Header