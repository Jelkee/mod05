import axios from "axios";

const state = {
  rooms: [],
};

const getters = {
  allRooms: (state) => state.rooms,
  nextRoomID: (state) => state.rooms.length,
  getRoom: (state) => (id) => state.rooms[id],
};

const actions = {
  async retrieveRooms({ commit }) {
    let response = await axios.get("http://localhost:3000/rooms"); //See proxy in vue.config.js
    let data = response.data;
    commit("setRooms", data);
  },

  async addRoom({ commit }, roomName) {
    let newRoom = { id: this.nextRoomID, name: roomName };
    let res = await axios.post("http://localhost:3000/rooms", newRoom);
    res.status === 201 ? commit("addRoom", newRoom) : alert("An error occured");
  },

  async editRoom({ commit }, room) {
    let res = await axios.put(`http://localhost:3000/rooms/${room.id}`, room);
    commit("editRoom", res.data);
  },

  async deleteRoom({ commit }, id) {
    let res = await axios.delete(`http://localhost:3000/rooms/${id}`);
    res.status === 200 ? commit("deleteRoom", id) : alert("An error occured");
  },
};

const mutations = {
  setRooms: (state, rooms) => (state.rooms = rooms),
  addRoom: (state, newRoom) => state.rooms.push(newRoom),
  editRoom: (state, room) => (state.rooms[room.id] = room),
  deleteRoom: (state, id) =>
    (state.rooms = state.rooms.filter((room) => room.id !== id)),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
