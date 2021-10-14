<template>
  <div>
    <button @click="toggleAddRoom">
      {{ !this.showAddRoom ? "Add room" : "Hide" }}
    </button>
    <AddRoom v-if="showAddRoom" @add-room="addRoom" />
    <Rooms />
    <SmartComponents />
    <Messages />
    <AddUser />
    <Users />
  </div>
</template>

<script>
import SmartComponents from "../components/SmartComponents.vue";
import Rooms from "../components/Rooms.vue";
import Messages from "../components/Messages.vue";
import AddRoom from "../components/AddRoom.vue";
import Users from "../components/Users.vue";
import AddUser from "../components/AddUser.vue";

export default {
  name: "Dashboard",
  components: { SmartComponents, Rooms, Messages, AddRoom, Users, AddUser },
  data() {
    return {
      showAddRoom: false,
    };
  },
  toggleAddRoom() {
    this.showAddRoom = !this.showAddRoom;
  },
};
</script>
