import path from "path";
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";


export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd());
    
  return {
    server: {
      proxy: {
        "/api/v1": {
          target: env.VITE_API_URL,
          changeOrigin: true,
          secure: false,
        },
      },
      host: true,
      strictPort: true,
      port: 5173,
      watch: {
        usePolling: true,
      },
    },
    resolve: {
      alias: {
        "@src": path.resolve(__dirname, "./src"),
        "@tests": path.resolve(__dirname, "./tests"),
      },
    },
    plugins: [react()],
  };
});