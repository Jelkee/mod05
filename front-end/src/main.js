import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import "./assets/css/theme.css";
import "./assets/css/main.css";
import "@fortawesome/fontawesome-free/css/all.css";

createApp(App)
  .use(router)
  .use(store)
  .mount("#app");
