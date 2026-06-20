import { useState,useEffect } from "react";
import api from "../api/axios";
import { useParams,useNavigate } from "react-router-dom";


function DatasetPage(){
    const navigate = useNavigate()
    const [fields,setFields] = useState([])
    const [fieldName,setFieldName] = useState("")
    const [fieldType,setFieldType] = useState("")
    const {projectID} = useParams()
    const [editID, setEditID] = useState(null)


    const fetchFields = async() =>{
        try {
            const token = localStorage.getItem("access")
            const response = await api.get(`/datasets/list/${projectID}/`, {headers:{Authorization:`Bearer ${token}`}})
            setFields(response.data)
            console.log(response.data)
        }
        catch(error){
            console.log(error)
        }
    }

    useEffect(() => { fetchFields() },[projectID])

    const handleCreateField = async() =>{
        try {
            const token = localStorage.getItem("access")
            const response = await api.post(`datasets/create/${projectID}/`,{field_name: fieldName, field_type:fieldType},{headers:{Authorization: `Bearer ${token}`}})
            console.log(response.data)
            fetchFields()
            setFieldName("")
            setFieldType("")
        }
        catch(error){
            console.log(error)
        }
    }

    const handleDeleteField =async(fieldID)=>{
        try{
            const token = localStorage.getItem("access")
            const response = await api.delete(`datasets/delete/${fieldID}/`,{headers:{Authorization:`Bearer ${token}`}})
            console.log(response.data)
            await fetchFields()
        }
        catch(error){ console.log(error)}
    }

    const handleGetField = async(projectID) =>{
        try{
            const token = localStorage.getItem("access")
            const response = await api.get(`datasets/list/${projectID}/`,{headers:{Authorization:`Bearer ${token}`}})
            console.log(response.data)
        }
        catch(error){console.log(error)}

    }
    const handleUpdateField = async() =>{
        try{
            const token = localStorage.getItem("access")
            const response = await api.patch(`/datasets/update/${editID}/`,{field_name: fieldName,field_type:fieldType},{headers:{Authorization: `Bearer ${token}`}})
            console.log(response.data)
            fetchFields()
            setFieldName("")
            setFieldType("")
            setEditID(null)
        }
        catch(error){console.log(error)}
    }
    const handleEditField = (field)=>
         {setFieldName(field.field_name),setFieldType(field.field_type),setEditID(field.id)}
    return(
        <>
        <h1>DATASET PAGE</h1>
      
        <input
        type="text"
        placeholder="Field Name"
        value={fieldName}
        onChange={(e)=> setFieldName(e.target.value)}></input>
        <select
        value={fieldType}
        onChange={(e)=> setFieldType(e.target.value)}>
            <option value="">Select Type</option>
            <option value="string">String</option>
            <option value="number">Number</option>
            <option value="date">Date</option>
            <option value="email">Email</option>
            <option value="boolean">Boolean</option>
            <option value="choice">Choice</option>
        </select>
        <button onClick={editID ? handleUpdateField : handleCreateField}>
                        {editID ? "update Field": "Create Field"}</button>
       {fields.map((field) => (
                         <li key={field.id}>
                         <h3>{field.field_name}</h3>

                          <button onClick={() => handleEditField(field)} > Edit </button>
                          <button onClick={() => handleDeleteField(field.id)} > Delete </button>
                         </li>
))}
        </>
    )
}
export default DatasetPage