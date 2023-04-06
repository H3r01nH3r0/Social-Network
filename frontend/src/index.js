import React from 'react';
import * as ReactDOMClient from "react-dom/client";
import App from './App';
import { UserProvider } from "./context/UserContext";
import './css/main.css';

const app = ReactDOMClient.createRoot(document.getElementById("root"))

app.render(
<UserProvider>
    <App />
</UserProvider>
)