import { useNavigate, useParams } from "react-router-dom";

import DashboardLayout from "../components/layout/DashboardLayout";

import PageHeader from "../components/common/PageHeader";
import SectionCard from "../components/common/SectionCard";
import LoadingSpinner from "../components/common/LoadingSpinner";
import EmptyState from "../components/common/EmptyState";

import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

import useUploads from "../hooks/useUploads";
import useDatasets from "../hooks/useDatasets";

import { useState } from "react";

import {
  Upload,
  FileSpreadsheet,
  Save,
  ArrowRight,
} from "lucide-react";

function UploadDataset() {

  const navigate = useNavigate();

  const { projectID } = useParams();

  const [selectedFile, setSelectedFile] = useState(null);

  const {
    uploadedDataset,
    preview,
    fields,
    loading,
    uploading,
    uploadDataset,
  } = useUploads(projectID);

  const {
    updateDatasetFields,
  } = useDatasets();

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {

    if (!selectedFile) {
      alert("Please select a CSV file.");
      return;
    }

    const formData = new FormData();

    formData.append("file", selectedFile);

    try {

      await uploadDataset(formData);

    } catch (err) {

      console.error(err);

    }

  };

  const handleSaveSchema = async () => {

    try {

      await updateDatasetFields(projectID, fields);

      alert("Schema saved successfully.");

    } catch (err) {

      console.error(err);

    }

  };

  if (loading) {
    return (
      <DashboardLayout>
        <LoadingSpinner text="Loading..." />
      </DashboardLayout>
    );
  }
  return (
  <DashboardLayout>

    <PageHeader
      title="Upload Dataset"
      description="Upload a dataset and configure its schema."
    />

    {/* Upload Section */}

    <SectionCard
      title="Upload CSV"
      description="Upload your dataset file."
    >

      <div className="space-y-5">

        <Input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
        />

        {selectedFile && (

          <div className="rounded-lg border p-4">

            <p className="font-semibold">
              {selectedFile.name}
            </p>

            <p className="text-sm text-muted-foreground">
              {(selectedFile.size / 1024).toFixed(2)} KB
            </p>

          </div>

        )}

        <Button
          onClick={handleUpload}
          disabled={uploading}
        >

          <Upload className="mr-2 h-4 w-4" />

          {uploading
            ? "Uploading..."
            : "Upload Dataset"}

        </Button>

      </div>

    </SectionCard>

    {/* Uploaded Dataset */}

    {uploadedDataset && (

      <SectionCard
        title="Dataset Information"
        description="Information about the uploaded dataset."
      >

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

          <div>

            <p className="text-sm text-muted-foreground">
              File
            </p>

            <p className="font-semibold">
              {uploadedDataset.file}
            </p>

          </div>

          <div>

            <p className="text-sm text-muted-foreground">
              Rows
            </p>

            <p className="font-semibold">
              {uploadedDataset.row_count}
            </p>

          </div>

          <div>

            <p className="text-sm text-muted-foreground">
              Columns
            </p>

            <p className="font-semibold">
              {uploadedDataset.column_count}
            </p>

          </div>

        </div>

      </SectionCard>

    )}

    {/* Preview */}

    {preview.length > 0 && (

      <SectionCard
        title="Dataset Preview"
        description="First 5 rows of the uploaded dataset."
      >

        <div className="overflow-x-auto">

          <table className="w-full border">

            <thead>

              <tr>

                {Object.keys(preview[0]).map((column) => (

                  <th
                    key={column}
                    className="border p-2 text-left"
                  >
                    {column}
                  </th>

                ))}

              </tr>

            </thead>

            <tbody>

              {preview.map((row, index) => (

                <tr key={index}>

                  {Object.values(row).map((value, i) => (

                    <td
                      key={i}
                      className="border p-2"
                    >
                      {String(value)}
                    </td>

                  ))}

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </SectionCard>

    )}

    {/* Detected Fields */}

    {fields.length > 0 && (

      <SectionCard
        title="Detected Fields"
        description="Automatically detected schema."
      >

        <div className="space-y-3">

          {fields.map((field, index) => (

            <div
              key={index}
              className="flex items-center justify-between rounded-lg border p-4"
            >

              <div>

                <p className="font-semibold">
                  {field.field_name}
                </p>

                <p className="text-sm text-muted-foreground">
                  {field.field_type}
                </p>

              </div>

            </div>

          ))}

        </div>

      </SectionCard>

    )}

    {/* Actions */}

    <SectionCard
      title="Next Step"
      description="Save schema and continue."
    >

      <div className="flex gap-4">

        <Button
          onClick={handleSaveSchema}
        >

          <Save className="mr-2 h-4 w-4" />

          Save Schema

        </Button>

        <Button
          variant="outline"
          onClick={() =>
            navigate(`/projects/${projectID}/generator`)
          }
        >

          Continue

          <ArrowRight className="ml-2 h-4 w-4" />

        </Button>

      </div>

    </SectionCard>

  </DashboardLayout>
);
}

export default UploadDataset;