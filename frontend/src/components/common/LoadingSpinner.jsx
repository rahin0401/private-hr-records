import { LoaderCircle } from "lucide-react";

function LoadingSpinner({
  text = "Loading...",
  size = 40,
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-12">

      <LoaderCircle
        size={size}
        className="animate-spin text-primary"
      />

      <p className="text-sm text-muted-foreground">
        {text}
      </p>

    </div>
  );
}

export default LoadingSpinner;