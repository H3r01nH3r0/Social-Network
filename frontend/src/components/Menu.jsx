import React, { useState } from "react";
import { IoIosHome, IoIosSettings, IoIosPerson } from 'react-icons/io';
import { TbMessageCircle2Filled } from "react-icons/tb"

const Menu = () => {
    const [active, setActive] = useState("wall-btn");
    
    const handleClick = (id) => {
        setActive(id);
    };
    
    const menuItems = [
        {
            id: "wall-btn",
            href: "#",
            icon: <IoIosHome />,
            label: "Home",
        },
        {
            id: "chats-btn",
            href:"#",
            icon: <TbMessageCircle2Filled />,
            label: "Messages"
        },
        {
            id: "profile-btn",
            href: "#",
            icon: <IoIosPerson />,
            label: "Profile",
        },
        {
            id: "settings-btn",
            href: "#",
            icon: <IoIosSettings />,
            label: "Settings",
        },
    ]

    return (
        <div className="menu-container">
            <ul>
            {menuItems.map((item) => (
                <li key={item.id}>
                    <a 
                        href={item.href}
                        id={item.id}
                        className={active === item.id ? "active": ""}
                        // onClick={() => handleClick(item.id)}
                    >
                        <span className="icon">{item.icon}</span>
                        <span>{item.label}</span>
                    </a>
                </li>
            ))}
            </ul>
        </div>
    )
}

export default Menu