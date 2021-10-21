import axios from "axios";

const state = { components: [] };

const getters = {
  allComponents: (state) => state.components,
  getComponents: (state) => (id) => {
    return state.components.filter((component) => component.roomId === id);
  },
};

const actions = {
  async retrieveComponents({ commit }) {
    let response = await axios.get("http://localhost:3000/components");
    let data = response.data;
    commit("setComponents", data);
  },
};

const mutations = {
  setComponents: (state, components) => (state.components = components),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
