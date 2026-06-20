import {useState} from 'react'
import axios from '../api/axios.js'
import {useNavigate} from "react-router-dom"



function Login() {
    const [username, setUsername] = useState('');
    const navigate = useNavigate();
    const [password, setPassword] = useState('');
    const handleSubmit = async () =>{
        try {
            const response = await axios.post('/accounts/login/', { username, password });
            localStorage.setItem('access', response.data.access);
            localStorage.setItem('refresh', response.data.refresh);
            console.log(response.data);
            navigate("/dashboard")

        } catch (error) {
            console.log(error);
        }
    };
    return (
        <>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleSubmit}>Login</button>
        </>
    )
}

export default Login