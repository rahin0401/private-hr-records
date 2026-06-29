import { useEffect, useState } from "react";
import api from "../api/axios";

function useProject(projectID) {
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getToken = () => ({
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
  });

  // Fetch Project Details
  const fetchProject = async () => {
    if (!projectID) return;

    setLoading(true);
    setError(null);

    try {
      const response = await api.get(
        `/projects/${projectID}/`,
        getToken()
      );

      setProject(response.data);

      return response.data;
    } catch (err) {
      console.error(err);
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Update Project
  const updateProject = async (projectData) => {
    try {
      const response = await api.patch(
        `/projects/${projectID}/update/`,
        projectData,
        getToken()
      );

      await fetchProject();

      return response.data;
    } catch (err) {
      console.error(err);
      setError(err);
      throw err;
    }
  };

  // Delete Project
  const deleteProject = async () => {
    try {
      await api.delete(
        `/projects/${projectID}/delete/`,
        getToken()
      );
    } catch (err) {
      console.error(err);
      setError(err);
      throw err;
    }
  };

  useEffect(() => {
    fetchProject();
  }, [projectID]);

  return {
    project,
    loading,
    error,

    fetchProject,
    updateProject,
    deleteProject,
  };
}

export default useProject;