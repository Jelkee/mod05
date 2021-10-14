import axios from "axios";

const state = {
  rooms: [],
};

const getters = {
  allRooms: (state) => state.rooms,
  nextRoomID: (state) => state.rooms.length,
  getRoom: (state, id) => state.users[id],
};

const actions = {
  async retrieveRooms({ commit }) {
    let response = await axios.get(`api/rooms`); //See proxy in vue.config.js
    let data = response.data;
    commit("setRooms", data);
  },

  async addRoom({ commit }, roomName) {
    let newRoom = { id: this.nextRoomID, name: roomName };
    let res = await axios.post("api/rooms", newRoom);
    res.status === 201 ? commit("addRoom", newRoom) : alert("An error occured");
  },

  async deleteRoom({ commit }, id) {
    let res = await axios.delete(`api/rooms/${id}`);
    res.status === 200 ? commit("deleteRoom", id) : alert("An error occured");
  },
};

const mutations = {
  setRooms: (state, rooms) => (state.rooms = rooms),
  addRoom: (state, newRoom) => state.rooms.push(newRoom),
  deleteRoom: (state, id) =>
    (state.rooms = state.rooms.filter((room) => room.id !== id)),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
