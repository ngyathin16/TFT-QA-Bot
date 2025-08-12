import type { Config } from "tailwindcss";
import jsConfig from "./tailwind.config.js";

const config: Config = jsConfig as unknown as Config;
export default config;