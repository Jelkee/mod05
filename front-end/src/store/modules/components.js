import axios from "axios";

const state = { components: [] };

const getters = {
  allComponents: (state) => state.components,
};

const actions = {
  async retrieveComponents({ commit }) {
    let response = await axios.get(`api/components`);
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
