import Sidebar from "./Sidebar";
import Navbar from "./Navbar";
import PageContainer from "./PageContainer";

function DashboardLayout({ children }) {
  return (
    <div className="flex min-h-screen bg-background">

      {/* Sidebar */}
      <Sidebar />

      {/* Main Area */}
      <div className="flex flex-1 flex-col overflow-hidden">

        {/* Top Navigation */}
        <Navbar />

        {/* Page Content */}
        <PageContainer>
          {children}
        </PageContainer>

      </div>

    </div>
  );
}

export default DashboardLayout;