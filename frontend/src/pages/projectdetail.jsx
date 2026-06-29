import { useNavigate, useParams } from "react-router-dom";

import DashboardLayout from "../components/layout/DashboardLayout";

import PageHeader from "../components/common/PageHeader";
import SectionCard from "../components/common/SectionCard";
import LoadingSpinner from "../components/common/LoadingSpinner";
import EmptyState from "../components/common/EmptyState";

import ProjectStatsCard from "../components/projects/ProjectStatsCard";
import QuickActionCard from "../components/projects/QuickActionCard";

import useProject from "../hooks/useProject";

import {
  Database,
  Upload,
  TableProperties,
  BrainCircuit,
  BarChart3,
  History,
  Shield,
  Calendar,
} from "lucide-react";

function ProjectDetail() {

  const navigate = useNavigate();

  const { projectID } = useParams();

  const {
    project,
    loading,
    error,
  } = useProject(projectID);

  if (loading) {
    return (
      <DashboardLayout>
        <LoadingSpinner text="Loading Project..." />
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>

        <EmptyState
          icon={Database}
          title="Unable to load project"
          description="An unexpected error occurred."
        />

      </DashboardLayout>
    );
  }

    if (!project) {
    return (
        <DashboardLayout>
            <EmptyState
                icon={Database}
                title="Project not found"
                description="The requested project does not exist."
            />
        </DashboardLayout>
    );
}
    return (
  <DashboardLayout>

    <PageHeader
      title={project.name}
      description={project.description}
    />

    {/* Project Information */}

    <SectionCard
      title="Project Information"
      description="Basic information about this project."
    >

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">

        <div>

          <p className="text-sm text-muted-foreground">
            Project Name
          </p>

          <h3 className="mt-1 text-lg font-semibold">
            {project.name}
          </h3>

        </div>

        <div>

          <p className="text-sm text-muted-foreground">
            Description
          </p>

          <h3 className="mt-1 text-lg">
            {project.description || "No description provided."}
          </h3>

        </div>

        <div className="flex items-center gap-2">

          <Calendar size={18} />

          <div>

            <p className="text-sm text-muted-foreground">
              Created
            </p>

            <p>
              {new Date(project.created_at).toLocaleString()}
            </p>

          </div>

        </div>

        <div className="flex items-center gap-2">

          <Calendar size={18} />

          <div>

            <p className="text-sm text-muted-foreground">
              Updated
            </p>

            <p>
              {new Date(project.updated_at).toLocaleString()}
            </p>

          </div>

        </div>

      </div>

    </SectionCard>

    {/* Statistics */}

    <div className="my-8 grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">

      <ProjectStatsCard
        title="Datasets"
        value="0"
        subtitle="Coming Soon"
        icon={Database}
      />

      <ProjectStatsCard
        title="Generated"
        value="0"
        subtitle="Coming Soon"
        icon={BrainCircuit}
      />

      <ProjectStatsCard
        title="Quality"
        value="--"
        subtitle="Coming Soon"
        icon={BarChart3}
      />

      <ProjectStatsCard
        title="Privacy"
        value="--"
        subtitle="Coming Soon"
        icon={Shield}
      />

    </div>

    {/* Quick Actions */}

    <SectionCard
      title="Quick Actions"
      description="Navigate to project modules."
    >

      <div className="grid grid-cols-1 gap-5 md:grid-cols-2">

        <QuickActionCard
          title="Upload Dataset"
          description="Upload CSV or Excel datasets."
          icon={Upload}
          onClick={() =>
            navigate(`/projects/${projectID}/upload`)
          }
        />

        <QuickActionCard
          title="Schema Management"
          description="Configure dataset schema."
          icon={TableProperties}
          onClick={() =>
            navigate(`/projects/${projectID}/schema`)
          }
        />

        <QuickActionCard
          title="Generator"
          description="Generate synthetic data."
          icon={BrainCircuit}
          onClick={() =>
            navigate(`/projects/${projectID}/generator`)
          }
        />

        <QuickActionCard
          title="Generation Results"
          description="View generated datasets."
          icon={History}
          onClick={() =>
            navigate(`/projects/${projectID}/generate`)
          }
        />

      </div>

    </SectionCard>

  </DashboardLayout>
);}
export default ProjectDetail