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

  async addUser({ commit }, name) {
    let response = await axios.post("api/users", {
      id: this.state.users.length,
      name: name,
    });
    let data = response.data;
    commit("addUser", data);
  },
};

const mutations = {
  setUsers: (state, users) => (state.users = users),
  addUser: (state, newUser) => state.users.push(newUser),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
