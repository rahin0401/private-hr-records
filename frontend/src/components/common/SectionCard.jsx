import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

function SectionCard({
  title,
  description,
  children,
  action,
}) {
  return (
    <Card className="shadow-sm">

      {(title || description || action) && (
        <CardHeader className="flex flex-row items-center justify-between">

          <div>

            {title && (
              <CardTitle className="text-xl">
                {title}
              </CardTitle>
            )}

            {description && (
              <p className="mt-1 text-sm text-muted-foreground">
                {description}
              </p>
            )}

          </div>

          {action && (
            <div>
              {action}
            </div>
          )}

        </CardHeader>
      )}

      <CardContent>
        {children}
      </CardContent>

    </Card>
  );
}

export default SectionCard;