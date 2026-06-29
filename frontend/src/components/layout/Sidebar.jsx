import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  FolderOpen,
  Database,
  TableProperties,
  BrainCircuit,
  BarChart3,
  History,
  Settings,
} from "lucide-react";

const menuItems = [
  {
    name: "Dashboard",
    icon: LayoutDashboard,
    path: "/dashboard",
  },
  {
    name: "Projects",
    icon: FolderOpen,
    path: "/dashboard",
  },
  {
    name: "Datasets",
    icon: Database,
    path: "/dashboard",
  },
  {
    name: "Schema",
    icon: TableProperties,
    path: "/dashboard",
  },
  {
    name: "Generator",
    icon: BrainCircuit,
    path: "/dashboard",
  },
  {
    name: "Analysis",
    icon: BarChart3,
    path: "/dashboard",
  },
  {
    name: "History",
    icon: History,
    path: "/dashboard",
  },
  {
    name: "Settings",
    icon: Settings,
    path: "/dashboard",
  },
];

function Sidebar() {
  return (
    <aside className="w-64 min-h-screen border-r bg-background">

      <div className="border-b p-6">

        <h1 className="text-2xl font-bold">
          SynthAI
        </h1>

        <p className="text-sm text-muted-foreground">
          Synthetic Data Platform
        </p>

      </div>

      <nav className="flex flex-col gap-2 p-4">

        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-4 py-3 transition-colors ${
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "hover:bg-muted"
                }`
              }
            >
              <Icon size={20} />

              <span>{item.name}</span>
            </NavLink>
          );
        })}

      </nav>
    </aside>
  );
}

export default Sidebar;