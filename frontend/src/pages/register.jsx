import{useState} from 'react'
import axios from '../api/axios.js'
import {useNavigate} from "react-router-dom"

function Register(){
 const [username, setUsername] = useState('');
 const [email, setEmail] = useState('');
 const [password, setPassword] = useState('');
 const navigate = useNavigate();
 const handleSubmit = async () =>{
        try {
            const response = await axios.post('/accounts/register/', { username, email, password });
            console.log(response.data);
              navigate("/login")

        }
        catch (error) {
            console.log(error);
        }
 }

    return (
        <>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleSubmit}>Register</button>
        </>
    )
}
export default Register