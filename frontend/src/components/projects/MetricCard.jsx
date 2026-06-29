import { Card, CardContent } from "../ui/card";

function MetricCard({
  title,
  value,
  icon: Icon,
}) {
  return (
    <Card className="transition-all duration-300 hover:shadow-lg hover:-translate-y-1">

      <CardContent className="flex items-center justify-between p-6">

        <div>

          <p className="text-sm text-muted-foreground">
            {title}
          </p>

          <h2 className="mt-2 text-3xl font-bold">
            {value}
          </h2>

        </div>

        <div className="rounded-xl bg-primary/10 p-4">

          <Icon
            size={28}
            className="text-primary"
          />

        </div>

      </CardContent>

    </Card>
  );
}

export default MetricCard;