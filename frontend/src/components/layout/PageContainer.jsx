function PageContainer({ children }) {
  return (
    <main className="flex-1 overflow-y-auto p-6 lg:p-8 bg-slate-950">
      <div className="mx-auto w-full max-w-7xl">
        {children}
      </div>
    </main>
  );
}

export default PageContainer;