import { Card, CardContent } from "../ui/card";
import { ArrowRight } from "lucide-react";

function QuickActionCard({
  title,
  description,
  icon: Icon,
  onClick,
}) {
  return (
    <Card
      onClick={onClick}
      className="
        cursor-pointer
        transition-all
        duration-300
        hover:-translate-y-1
        hover:shadow-lg
      "
    >
      <CardContent className="flex items-center justify-between p-6">

        <div className="flex items-center gap-4">

          <div className="rounded-xl bg-primary/10 p-3">

            {Icon && (
              <Icon
                className="text-primary"
                size={24}
              />
            )}

          </div>

          <div>

            <h3 className="text-lg font-semibold">
              {title}
            </h3>

            <p className="text-sm text-muted-foreground">
              {description}
            </p>

          </div>

        </div>

        <ArrowRight
          className="text-muted-foreground"
          size={22}
        />

      </CardContent>
    </Card>
  );
}

export default QuickActionCard;