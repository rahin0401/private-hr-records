import { useState } from "react";
import { useNavigate } from "react-router-dom";

import DashboardLayout from "../components/layout/DashboardLayout";

import MetricCard from "../components/projects/MetricCard";
import ProjectCard from "../components/projects/ProjectCard";
import ProjectForm from "../components/projects/ProjectForm";

import PageHeader from "../components/common/PageHeader";
import SectionCard from "../components/common/SectionCard";
import EmptyState from "../components/common/EmptyState";
import LoadingSpinner from "../components/common/LoadingSpinner";
import SearchBar from "../components/common/SearchBar";

import {
  FolderOpen,
  BarChart3,
  Shield,
  Database,
  Plus,
} from "lucide-react";

import api from "../api/axios";

import useProjects from "../hooks/useProjects";
import useDashboard from "../hooks/useDashboard";

function Dashboard() {

  const navigate = useNavigate();

  const {
    projects,
    loading: projectsLoading,
    error: projectsError,
    createProject,
    updateProject,
    deleteProject,
  } = useProjects();

  const {
    dashboardStats,
    loading: dashboardLoading,
    error: dashboardError,
  } = useDashboard();

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [editId, setEditId] = useState(null);
  const [search, setSearch] = useState("");

  const handleCreateProject = async () => {
  try {
    await createProject({
      name,
      description,
    });

    setName("");
    setDescription("");
  } catch (error) {
    console.error(error);
  }
};

const handleUpdateProject = async () => {
  try {
    await updateProject(editId, {
      name,
      description,
    });

    setName("");
    setDescription("");
    setEditId(null);
  } catch (error) {
    console.error(error);
  }
};

const handleDeleteProject = async (id) => {
  try {
    await deleteProject(id);
  } catch (error) {
    console.error(error);
  }
};

const handleEditProject = (project) => {
  setName(project.name);
  setDescription(project.description);
  setEditId(project.id);
};

const handleLogout = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  navigate("/login");
};

const handleGetProfile = async () => {
  try {
    const token = localStorage.getItem("access");

    const response = await api.get("/accounts/profile/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
};
return (
  <DashboardLayout>

    <PageHeader
      title="Dashboard"
      description="Manage your synthetic data projects"
      buttonText="Get Profile"
      buttonIcon={Plus}
      onButtonClick={handleGetProfile}
    />

    {/* Metric Cards */}

    <div className="mb-8 grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">

      <MetricCard
        title="Projects"
        value={dashboardStats?.total_projects || 0}
        icon={FolderOpen}
      />

      <MetricCard
        title="Quality Score"
        value={dashboardStats?.average_quality_score || 0}
        icon={BarChart3}
      />

      <MetricCard
        title="Privacy Score"
        value={dashboardStats?.average_privacy_score || 0}
        icon={Shield}
      />

      <MetricCard
        title="Datasets"
        value={dashboardStats?.total_datasets || 0}
        icon={Database}
      />

    </div>

    {/* Search */}

    <div className="mb-6 flex justify-between">

      <SearchBar
        value={search}
        onChange={setSearch}
        onClear={() => setSearch("")}
        placeholder="Search Projects..."
      />

    </div>

    {/* Project Form */}

    <div className="mb-8">

      <ProjectForm
        name={name}
        description={description}
        setName={setName}
        setDescription={setDescription}
        editId={editId}
        onSubmit={
          editId
            ? handleUpdateProject
            : handleCreateProject
        }
      />

    </div>

    {/* Recent Projects */}

    <SectionCard
      title="Recent Projects"
      description="Manage all your projects"
    >

      {projectsLoading ? (

        <LoadingSpinner text="Loading Projects..." />

      ) : projects.length === 0 ? (

        <EmptyState
          icon={FolderOpen}
          title="No Projects Found"
          description="Create your first project to get started."
          buttonText="Create Project"
        />

      ) : (

        <div className="grid gap-5">

          {projects
            .filter((project) =>
              project.name
                .toLowerCase()
                .includes(search.toLowerCase())
            )
            .map((project) => (

              <ProjectCard
                key={project.id}
                project={project}
                onOpen={(id) =>
                  navigate(`/projects/${id}`)
                }
                onEdit={handleEditProject}
                onDelete={handleDeleteProject}
              />

            ))}

        </div>

      )}

    </SectionCard>

  </DashboardLayout>
);}
export default Dashboard