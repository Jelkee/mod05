<template>
  <div>
    <button @click="toggleAddRoom">
      {{ !this.showAddRoom ? "Add room" : "Hide" }}
    </button>
    <AddRoom v-if="showAddRoom" @add-room="addRoom" />
    <Rooms :rooms="rooms" @edit-room="editRoom" @delete-room="deleteRoom" />
    <SmartComponents :smart_components="smart_components" />
    <Messages :messages="messages" />
    <Users />
  </div>
</template>

<script>
import axios from "axios";
import SmartComponents from "../components/SmartComponents.vue";
import Rooms from "../components/Rooms.vue";
import Messages from "../components/Messages.vue";
import AddRoom from "../components/AddRoom.vue";
import Users from "../components/Users.vue";

export default {
  name: "Dashboard",
  components: { SmartComponents, Rooms, Messages, AddRoom, Users },
  data() {
    return {
      rooms: [],
      smart_components: [],
      messages: [],
      showAddRoom: false,
    };
  },
  methods: {
    async retrieveData(item_name) {
      let response = await axios.get(`api/${item_name}`); //See proxy in vue.config.js
      let data = response.data;
      return data;
    },
    toggleAddRoom() {
      this.showAddRoom = !this.showAddRoom;
    },
    async addRoom(roomName) {
      let newRoom = { id: this.rooms.length, name: roomName };
      let res = await axios.post("api/rooms", newRoom);
      res.status === 201 ? this.rooms.push(newRoom) : alert("An error occured");
    },
    async deleteRoom(id) {
      let res = await axios.delete(`api/rooms/${id}`);
      res.status === 200
        ? (this.rooms = this.rooms.filter((room) => room.id !== id))
        : alert("An error occured");
      this.rooms = this.rooms.filter((room) => room.id !== id);
    },
  },
  computed: {
    nextID: function() {
      return this.rooms.length;
    },
  },
  async created() {
    this.rooms = await this.retrieveData("rooms");
    this.smart_components = await this.retrieveData("smart_components");
    this.messages = await this.retrieveData("messages");
  },
};
</script>
