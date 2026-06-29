import { BrowserRouter, Routes, Route } from "react-router-dom";

import "./App.css";

import Login from "./pages/login";
import Register from "./pages/register";
import ProtectedRoute from "./pages/protectedroute";

import Dashboard from "./pages/dashboard";
import ProjectDetail from "./pages/projectdetail";

import UploadDataset from "./pages/uploadDataset";
import SchemaManagement from "./pages/schemamanagement";
import Generator from "./pages/generator";
import GenerateSyntheticDataset from "./pages/generatesyntheticdataset";

function App() {
  return (
    <BrowserRouter>

      <Routes>

        {/* Redirect Login */}
        <Route
          path="/"
          element={<Login />}
        />

        {/* Authentication */}

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        {/* Dashboard */}

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        {/* Project Home */}

        <Route
          path="/projects/:projectID"
          element={
            <ProtectedRoute>
              <ProjectDetail />
            </ProtectedRoute>
          }
        />

        {/* Upload Dataset */}

        <Route
          path="/projects/:projectID/upload"
          element={
            <ProtectedRoute>
              <UploadDataset />
            </ProtectedRoute>
          }
        />

        {/* Schema */}

        <Route
          path="/projects/:projectID/schema"
          element={
            <ProtectedRoute>
              <SchemaManagement />
            </ProtectedRoute>
          }
        />

        {/* Generator */}

        <Route
          path="/projects/:projectID/generator"
          element={
            <ProtectedRoute>
              <Generator />
            </ProtectedRoute>
          }
        />

        {/* Generation Result */}

        <Route
          path="/projects/:projectID/generate"
          element={
            <ProtectedRoute>
              <GenerateSyntheticDataset />
            </ProtectedRoute>
          }
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;