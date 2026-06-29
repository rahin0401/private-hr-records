import { Button } from "../ui/button";

function PageHeader({
  title,
  description,
  buttonText,
  onButtonClick,
  buttonIcon: ButtonIcon,
  children,
}) {
  return (
    <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">

      {/* Left */}
      <div>

        <h1 className="text-3xl font-bold tracking-tight">
          {title}
        </h1>

        {description && (
          <p className="mt-2 text-muted-foreground">
            {description}
          </p>
        )}

      </div>

      {/* Right */}
      <div className="flex items-center gap-3">

        {children}

        {buttonText && (
          <Button onClick={onButtonClick}>

            {ButtonIcon && (
              <ButtonIcon className="mr-2 h-4 w-4" />
            )}

            {buttonText}

          </Button>
        )}

      </div>

    </div>
  );
}

export default PageHeader;