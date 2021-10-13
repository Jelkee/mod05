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

const rooms = [
  { id: 0, name: "Living room" },
  { id: 1, name: "Kitchen" },
];

const smart_components = [
  { id: 0, roomID: 0, type: "light", name: "Light in living room" },
  {
    id: 1,
    roomID: 0,
    type: "light_sensor",
    name: "Light sensor in living room",
  },
  { id: 1, roomID: 1, type: "radiator", name: "Radiator in kitchen" },
];

const messages = [{ id: 0, body: "Hey, this is the first message!" }];

export default {
  name: "App",
  components: { SiteHeader, Rooms, SmartComponents, Messages, AddRoom },
  data() {
    return { rooms, smart_components, messages, showAddRoom: false };
  },
  methods: {
    addRoom(roomName) {
      this.rooms.push({ id: this.rooms.length, name: roomName });
    },
    toggleAddRoom() {
      this.showAddRoom = !this.showAddRoom;
    },
  },
  computed: {
    nextID: function() {
      return this.rooms.length;
    },
  },
};
</script>

<style></style>
