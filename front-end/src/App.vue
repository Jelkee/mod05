<template>
  <div>
    <SiteHeader />
    <button @click="toggleAddRoom">
      {{ !this.showAddRoom ? "Add room" : "Hide" }}
    </button>
    <AddRoom v-if="showAddRoom" @add-room="addRoom" />
    <Rooms :rooms="rooms" />
    <SmartComponents :smart_components="smart_components" />
    <Messages :messages="messages" />
  </div>
</template>

<script>
import SmartComponents from "./components/SmartComponents.vue";
import Rooms from "./components/Rooms.vue";
import SiteHeader from "./components/SiteHeader.vue";
import Messages from "./components/Messages.vue";
import AddRoom from "./components/AddRoom.vue";

const rooms = [];
const smart_components = [];
const messages = [];

export default {
  name: "App",
  components: { SiteHeader, Rooms, SmartComponents, Messages, AddRoom },
  data() {
    return { rooms, smart_components, messages, showAddRoom: false };
  },
  methods: {
    async addRoom(roomName) {
      let newRoom = { id: this.rooms.length, name: roomName };
      await fetch("api/rooms", {
        method: "POST",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify(newRoom),
      });
      this.rooms.push(newRoom);
    },
    toggleAddRoom() {
      this.showAddRoom = !this.showAddRoom;
    },
    async retrieveData(item_name) {
      const res = await fetch(`api/${item_name}`); //See proxy in vue.config.js
      const data = await res.json();
      return data;
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

<style></style>
