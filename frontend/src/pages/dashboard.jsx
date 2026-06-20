import api from "../api/axios"
import {useNavigate} from "react-router-dom"
import {useState,useEffect} from "react"

function Dashboard() {
    const navigate = useNavigate()
    const [projects, setProjects] = useState([])
    const [name, setName] = useState("")
    const [description, setDescription] = useState("")
    const [editId, setEditId] = useState(null)

    const fetchProjects = async () => {
        try {
            const token = localStorage.getItem("access")
            const response = await api.get("/projects/list/", { headers: { Authorization: `Bearer ${token}` } })
            setProjects(response.data)
            console.log(projects)
        } catch (error) {
            console.log(error)
        }
    }

    useEffect(() => {
        fetchProjects()
    }, [])

    const handleCreateProject = async () => {
        try {
            const token = localStorage.getItem("access")
            const response = await api.post("/projects/create/", { name, description }, { headers: { Authorization: `Bearer ${token}` } })
            console.log(response.data)
            fetchProjects() // Refresh the project list
            setName("")
            setDescription("")
        } catch (error) {
            console.log(error)
        }
    }

    const handleDeleteProject = async (Id) => {
        try{
            const token = localStorage.getItem("access")
            const response = await api.delete(`/projects/${Id}/delete/`, { headers: { Authorization: `Bearer ${token}` } })
            console.log(response.data)
            await fetchProjects() // Refresh the project list 
        } catch (error) {
            console.log(error)
        }
    }
    const handleGetProfile = async () => {

        try {

            const token =
                localStorage.getItem("access")

            const response =
                await api.get(
                    "/accounts/profile/",
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`
                        }
                    }
                )

            console.log(
                response.data
            )

        }
        catch(error) {

            console.log(error)

        }
    }
    const handleUpdateProject = async () => {
        try {
            const token = localStorage.getItem("access")
            const response = await api.patch(`/projects/${editId}/update/`, { name, description }, { headers: { Authorization: `Bearer ${token}` } })
            console.log(response.data)
            fetchProjects() // Refresh the project list 
            setName("")
            setDescription("")
            setEditId(null)
        } catch (error) {
            console.log(error)
        }
    }
    const handleEditProject = ( project) => { setName(project.name),setDescription(project.description),setEditId(project.id)}
    const handlelogout = () => {
        localStorage.removeItem("access")
        localStorage.removeItem("refresh")
        navigate("/login")
    }

    return (
        <>
            <h1>Dashboard Page</h1>

            <button
                onClick={handleGetProfile}
            >
                Get Profile
            </button>
            <button onClick={() => handlelogout()}>
                Logout
            </button>
            <input
                type="text"
                placeholder="Project Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
            <input
                type="text"
                placeholder="Project Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />
            <button
        onClick={editId ? handleUpdateProject : handleCreateProject}>
                {editId ? "Update Project" : "Create Project"}
            </button>
            <h2>my projects</h2>
            <ul>
                {projects.map((project) => (
                    <li key={project.id}>
                        <h3>{project.name}</h3>
                        <p>{project.description}</p>
                        <button onClick={() => handleDeleteProject(project.id)}>
                            Delete
                        </button>
                        <button onClick={() => handleEditProject(project)}>
                            Edit
                        </button>
                    </li>
                ))}
            </ul>
            <button onClick={()=> navigate(`/projects/${project.id}`)}>open</button>
        </>
    )
}

export default Dashboard