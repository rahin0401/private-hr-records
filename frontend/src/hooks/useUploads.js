import { useState } from "react";
import api from "../api/axios";

function useUploads(projectID) {
  const [uploads, setUploads] = useState([]);

  const [uploadedDataset, setUploadedDataset] = useState(null);

  const [preview, setPreview] = useState([]);

  const [fields, setFields] = useState([]);

  const [loading, setLoading] = useState(false);

  const [uploading, setUploading] = useState(false);

  const [error, setError] = useState(null);

  const getToken = () => ({
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
  });

  // Upload Dataset
  const uploadDataset = async (formData) => {
    try {
      setUploading(true);
      setError(null);

      const response = await api.post(
        `/uploads/upload/${projectID}/`,
        formData,
        {
          ...getToken(),
          headers: {
            ...getToken().headers,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      // Save response

      setUploadedDataset(response.data.dataset);

      setPreview(response.data.preview);

      setFields(response.data.fields);

      return response.data;

    } catch (err) {

      console.error(err);

      setError(err);

      throw err;

    } finally {

      setUploading(false);

    }
  };

  // Future Endpoint
  const fetchUploads = async () => {
    /*
      TODO

      GET /uploads/list/<projectID>/

      Not implemented in backend yet.
    */
  };

  // Future Endpoint
  const deleteUpload = async (uploadID) => {
    /*
      TODO

      DELETE /uploads/delete/<uploadID>/

      Not implemented in backend yet.
    */
  };

  return {

    uploads,

    uploadedDataset,

    preview,

    fields,

    loading,

    uploading,

    error,

    uploadDataset,

    fetchUploads,

    deleteUpload,
  };
}

export default useUploads;