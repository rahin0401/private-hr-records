import { Search, X } from "lucide-react";
import { Input } from "../ui/input";
import { Button } from "../ui/button";

function SearchBar({
  value,
  onChange,
  placeholder = "Search...",
  onClear,
}) {
  return (
    <div className="relative w-full max-w-md">

      <Search
        size={18}
        className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground"
      />

      <Input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="pl-10 pr-10"
      />

      {value && (
        <Button
          variant="ghost"
          size="icon"
          className="absolute right-1 top-1/2 -translate-y-1/2 h-8 w-8"
          onClick={onClear}
        >
          <X size={16} />
        </Button>
      )}

    </div>
  );
}

export default SearchBar;