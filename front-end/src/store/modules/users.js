import axios from "axios";

const state = {
  users: [],
};
const getters = {
  allUsers: (state) => state.users,
};
const actions = {
  async retrieveUsers({ commit }) {
    let response = await axios.get("api/users");
    let data = response.data;
    commit("setUsers", data);
  },
  /*async addUser({ commit }, name) {
    const response = await axios.post("api/users", {
      id: this.users.length,
      name: name,
    });
  },*/
};
const mutations = {
  setUsers: (state, users) => (state.users = users),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
