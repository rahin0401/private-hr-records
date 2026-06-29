import { Card, CardContent } from "../ui/card";
import { Button } from "../ui/button";
import {
  FolderOpen,
  Pencil,
  Trash2,
  ArrowRight,
} from "lucide-react";

function ProjectCard({
  project,
  onOpen,
  onEdit,
  onDelete,
}) {
  return (
    <Card className="transition-all duration-300 hover:shadow-lg hover:-translate-y-1">

      <CardContent className="space-y-5 p-6">

        {/* Header */}
        <div className="flex items-start justify-between">

          <div className="flex items-center gap-3">

            <div className="rounded-xl bg-primary/10 p-3">

              <FolderOpen
                size={24}
                className="text-primary"
              />

            </div>

            <div>

              <h3 className="text-lg font-semibold">
                {project.name}
              </h3>

              <p className="text-sm text-muted-foreground">
                {project.description}
              </p>

            </div>

          </div>

        </div>

        {/* Actions */}
        <div className="flex items-center justify-end gap-2">

          <Button
            variant="outline"
            onClick={() => onOpen(project.id)}
          >
            <ArrowRight className="mr-2 h-4 w-4" />
            Open
          </Button>

          <Button
            variant="secondary"
            onClick={() => onEdit(project)}
          >
            <Pencil className="mr-2 h-4 w-4" />
            Edit
          </Button>

          <Button
            variant="destructive"
            onClick={() => onDelete(project.id)}
          >
            <Trash2 className="mr-2 h-4 w-4" />
            Delete
          </Button>

        </div>

      </CardContent>

    </Card>
  );
}

export default ProjectCard;