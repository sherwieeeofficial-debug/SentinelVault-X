import {useState} from "react";
import api from "../services/api";


function Login({onLogin}){


const [username,setUsername]=useState("");

const [password,setPassword]=useState("");

const [message,setMessage]=useState("");



async function handleLogin(){


try{


const formData = new FormData();


formData.append(
"username",
username
);


formData.append(
"password",
password
);



const response = await api.post(

"/login",

formData

);



localStorage.setItem(

"token",

response.data.access_token

);



setMessage(
"✅ Login Successful"
);



setTimeout(()=>{

onLogin();

},500);



}

catch(error){


setMessage(
"❌ Login Failed"
);


}



}



return (

<div>


<h1>
🔐 SentinelVault X
</h1>


<input

placeholder="Username"

onChange={e=>setUsername(e.target.value)}

/>


<br/>


<input

type="password"

placeholder="Password"

onChange={e=>setPassword(e.target.value)}

/>


<br/><br/>


<button onClick={handleLogin}>

Login

</button>


<h3>

{message}

</h3>


</div>

)


}


export default Login;
