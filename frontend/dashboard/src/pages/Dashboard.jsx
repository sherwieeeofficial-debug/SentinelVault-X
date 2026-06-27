import {useState,useEffect} from "react";
import api from "../services/api";

import {

LineChart,
Line,
XAxis,
YAxis,
CartesianGrid,
Tooltip

} from "recharts";



function Dashboard(){


const [status,setStatus]=useState({});

const [events,setEvents]=useState([]);

const [chart,setChart]=useState([]);





async function loadData(){


const token=localStorage.getItem("token");


const config={

headers:{

Authorization:

`Bearer ${token}`

}

};



try{


const statusRes=await api.get(

"/security-status",

config

);


setStatus(statusRes.data);




const eventRes=await api.get(

"/events",

config

);



setEvents(eventRes.data);




let graph=[];


eventRes.data.forEach(

(item,index)=>{


graph.push({

time:index+1,

security:

98-index

})


}

);



setChart(graph);



}

catch(err){

console.log(err);

}


}







useEffect(()=>{


loadData();



const timer=setInterval(

loadData,

5000

);



return ()=>clearInterval(timer);


},[]);






function logout(){


localStorage.removeItem("token");


window.location.reload();


}







return (

<div>



<h1>
🔐 SentinelVault X
</h1>


<h2>
Security Operations Center
</h2>


<hr/>





<h2>
🟢 System Status
</h2>


<h1>

{status.status}

</h1>





<h2>
🛡 Threat Level
</h2>


<h1>

{status.threat_level}

</h1>





<h2>
🔒 Encryption
</h2>


<h1>

{status.encryption}

</h1>






<h2>
📊 Security Score
</h2>


<h1>

{status.security_score}/100

</h1>







<h2>
📈 Security Analytics
</h2>



<LineChart

width={500}

height={250}

data={chart}

>


<CartesianGrid />

<XAxis dataKey="time"/>

<YAxis/>

<Tooltip/>

<Line

type="monotone"

dataKey="security"

/>


</LineChart>







<hr/>






<h2>
🧠 Security Events
</h2>




{

events.map(

(event,index)=>(


<div key={index}>


<p>
⏱ {event.time}
</p>


<p>
👤 {event.user}
</p>


<p>
🌐 {event.ip}
</p>


<p>
🚨 {event.event}
</p>


<hr/>


</div>


)

)


}






<button onClick={logout}>

Logout

</button>




</div>


)


}



export default Dashboard;
