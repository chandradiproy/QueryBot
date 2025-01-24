import { Bot } from "lucide-react";
import React from "react";

function Navbar() {
  return (
    <header className="md:w-3xl rounded-2xl shadow-2xl mt-2 w-full flex justify-between items-center dark:bg-zinc-900/90 bg-gray-200/20 backdrop-blur-3xl h-16 p-4">
      <div className="flex items-center gap-2">
        <Bot size={30} className="dark:text-white text-black" />
        <span className="dark:text-white text-black font-bold sm:block hidden">QueryBot</span>
      </div>
    </header>
  );
}

export default Navbar;
