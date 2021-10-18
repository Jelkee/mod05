import axios from "axios";

const state = {
  messages: [],
};

const getters = {
  allMessages: (state) => state.messages,
};

const actions = {
  async retrieveMessages({ commit }) {
    let response = await axios.get("http://localhost:3000/messages");
    let data = response.data;
    commit("setComponents", data);
  },
};

const mutations = {
  setMessages: (state, components) => (state.components = components),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
