const state = {
  authenticated: false,
};

const getters = {};

const actions = {
  login({ commit }) {
    commit("setAuthentication", true);
  },
  logout({ commit }) {
    commit("setAuthentication", false);
  },
};

const mutations = {
  setAuthentication: (state, status) => (state.authenticated = status),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
