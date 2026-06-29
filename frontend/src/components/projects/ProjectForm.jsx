import { Card, CardContent } from "../ui/card";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Textarea } from "../ui/textarea";

function ProjectForm({
  name,
  description,
  setName,
  setDescription,
  editId,
  onSubmit,
}) {
  return (
    <Card>

      <CardContent className="space-y-6 p-6">

        <div>

          <h2 className="text-xl font-semibold">
            {editId ? "Update Project" : "Create Project"}
          </h2>

          <p className="text-sm text-muted-foreground">
            Create and manage synthetic data projects.
          </p>

        </div>

        <div className="space-y-4">

          <Input
            placeholder="Project Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <Textarea
            placeholder="Project Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={4}
          />

        </div>

        <div className="flex justify-end">

          <Button
            onClick={onSubmit}
          >
            {editId ? "Update Project" : "Create Project"}
          </Button>

        </div>

      </CardContent>

    </Card>
  );
}

export default ProjectForm;