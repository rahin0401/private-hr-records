import { Badge } from "../ui/badge";

function StatusBadge({
  status,
}) {
  const statusStyles = {
    success: "bg-green-100 text-green-700 border-green-200",
    warning: "bg-yellow-100 text-yellow-700 border-yellow-200",
    danger: "bg-red-100 text-red-700 border-red-200",
    info: "bg-blue-100 text-blue-700 border-blue-200",
    pending: "bg-orange-100 text-orange-700 border-orange-200",
    default: "bg-muted text-muted-foreground",
  };

  return (
    <Badge
      variant="outline"
      className={statusStyles[status?.toLowerCase()] || statusStyles.default}
    >
      {status}
    </Badge>
  );
}

export default StatusBadge;