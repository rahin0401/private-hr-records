import { Bell, Search, User } from "lucide-react";
import { Input } from "../ui/input";
import { Button } from "../ui/button";

function Navbar() {
  return (
    <header className="flex h-16 items-center justify-between border-b bg-background px-6">

      {/* Left */}
      <div className="flex items-center gap-4">

        <h2 className="text-xl font-semibold">
          Dashboard
        </h2>

      </div>

      {/* Center */}
      <div className="hidden w-full max-w-md md:flex">

        <div className="relative w-full">

          <Search
            size={18}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground"
          />

          <Input
            placeholder="Search..."
            className="pl-10"
          />

        </div>

      </div>

      {/* Right */}
      <div className="flex items-center gap-3">

        <Button
          variant="ghost"
          size="icon"
        >
          <Bell size={20} />
        </Button>

        <Button
          variant="ghost"
          size="icon"
        >
          <User size={20} />
        </Button>

      </div>

    </header>
  );
}

export default Navbar;