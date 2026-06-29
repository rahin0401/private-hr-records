import { Button } from "../ui/button";

function EmptyState({
  icon: Icon,
  title,
  description,
  buttonText,
  onButtonClick,
}) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed py-16 text-center">

      {Icon && (
        <div className="mb-4 rounded-full bg-primary/10 p-4">
          <Icon className="h-10 w-10 text-primary" />
        </div>
      )}

      <h2 className="text-xl font-semibold">
        {title}
      </h2>

      <p className="mt-2 max-w-md text-sm text-muted-foreground">
        {description}
      </p>

      {buttonText && (
        <Button
          className="mt-6"
          onClick={onButtonClick}
        >
          {buttonText}
        </Button>
      )}

    </div>
  );
}

export default EmptyState;