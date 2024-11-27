import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import { OpenAPI } from "./client";

OpenAPI.BASE = import.meta.env.VITE_API_URL;

createApp(App).mount("#app");
