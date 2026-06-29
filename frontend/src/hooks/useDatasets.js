import { useState } from "react";
import api from "../api/axios";

function useDatasets() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getToken = () => ({
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
  });

  // Create Dataset Fields
  const createDatasetFields = async (projectID, data) => {
    try {
      setLoading(true);
      setError(null);

      const response = await api.post(
        `/datasets/create/${projectID}/`,
        data,
        getToken()
      );

      return response.data;
    } catch (err) {
      console.error(err);
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Fetch Dataset Fields
  const fetchDatasetFields = async (projectID) => {
    try {
      setLoading(true);
      setError(null);

      const response = await api.get(
        `/datasets/list/${projectID}/`,
        getToken()
      );

      return response.data;
    } catch (err) {
      console.error(err);
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Get One Dataset Field
  const getDatasetField = async (fieldID) => {
    try {
      const response = await api.get(
        `/datasets/detail/${fieldID}/`,
        getToken()
      );

      return response.data;
    } catch (err) {
      console.error(err);
      setError(err);
      throw err;
    }
  };

  // Update Dataset Fields
  const updateDatasetFields = async (projectID, data) => {
    try {
      setLoading(true);

      const response = await api.patch(
        `/datasets/fields/${projectID}/`,
        data,
        getToken()
      );

      return response.data;
    } catch (err) {
      console.error(err);
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Delete Dataset
  const deleteDataset = async (datasetID) => {
    try {
      await api.delete(
        `/datasets/delete/${datasetID}/`,
        getToken()
      );
    } catch (err) {
      console.error(err);
      setError(err);
      throw err;
    }
  };

  return {
    loading,
    error,

    createDatasetFields,
    fetchDatasetFields,
    getDatasetField,
    updateDatasetFields,
    deleteDataset,
  };
}

export default useDatasets;