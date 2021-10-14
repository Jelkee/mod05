import { createStore } from "vuex";
import users from "./modules/users";
import rooms from "./modules/rooms";
import components from "./modules/components";
import messages from "./modules/messages";

const store = createStore({ modules: { users, rooms, components, messages } });
export default store;
