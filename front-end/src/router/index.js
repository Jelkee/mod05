import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Dashboard from "../views/Dashboard.vue";
import Components from "../views/Components.vue";
import Rooms from "../views/Rooms.vue";

const routes = [
  { path: "/login", name: "Login", component: Login },
  { path: "/dashboard", name: "Dashboard", component: Dashboard },
  {
    path: "/dashboard/:id",
    name: "Room",
    component: Dashboard,
  },
  { path: "/components", name: "Components", component: Components },
  { path: "/rooms", name: "Rooms", component: Rooms },
];
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
