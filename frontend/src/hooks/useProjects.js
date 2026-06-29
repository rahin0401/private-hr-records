import { useEffect, useState } from "react";
import api from "../api/axios";

function useProjects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getToken = () => ({
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
  });

  // Fetch Projects
  const fetchProjects = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.get(
        "/projects/list/",
        getToken()
      );

      setProjects(response.data);
    } catch (err) {
      console.error(err);
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  // Create Project
  const createProject = async (projectData) => {
    try {
      const response = await api.post(
        "/projects/create/",
        projectData,
        getToken()
      );

      await fetchProjects();

      return response.data;
    } catch (err) {
      console.error(err);
      setError(err);
      throw err;
    }
  };

  // Update Project
  const updateProject = async (id, projectData) => {
    try {
      const response = await api.patch(
        `/projects/${id}/update/`,
        projectData,
        getToken()
      );

      await fetchProjects();

      return response.data;
    } catch (err) {
      console.error(err);
      setError(err);
      throw err;
    }
  };

  // Delete Project
  const deleteProject = async (id) => {
    try {
      await api.delete(
        `/projects/${id}/delete/`,
        getToken()
      );

      await fetchProjects();
    } catch (err) {
      console.error(err);
      setError(err);
      throw err;
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  return {
    projects,
    loading,
    error,

    fetchProjects,
    createProject,
    updateProject,
    deleteProject,
  };
}

export default useProjects;