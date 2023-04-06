import React, { useContext } from "react";
import Header from "./components/Header";
import Wall from "./components/Wall";
import Login from "./components/Login";
import { UserContext } from "./context/UserContext";


const App = () => {
  const [token] = useContext(UserContext);
  
  return (
    <div>
      <Header />
      {!token ? <Login /> : <Wall/>}
    </div>
  );
};

export default App;
