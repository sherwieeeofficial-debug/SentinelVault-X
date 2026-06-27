import {useState} from "react";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";


function App(){


const [token,setToken] = useState(

localStorage.getItem("token")

);



if(token){

return <Dashboard/>

}



return (

<Login onLogin={()=>{

setToken(

localStorage.getItem("token")

)

}}/>

);


}


export default App;
