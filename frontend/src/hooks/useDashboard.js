import { useEffect, useState } from "react";
import api from "../api/axios";

function useDashboard() {
  const [dashboardStats, setDashboardStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getToken = () => ({
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
  });

  // Fetch Dashboard Statistics
  const fetchDashboardStats = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.get(
        "/dashboard/stats/",
        getToken()
      );

      setDashboardStats(response.data);

      return response.data;
    } catch (err) {
      console.error(err);
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  return {
    dashboardStats,
    loading,
    error,

    fetchDashboardStats,
  };
}

export default useDashboard;