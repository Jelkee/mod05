<template>
  <ul class="nav">
    <li class="nav-item">
      <router-link to="/dashboard" class="nav-link active">
        Overview
      </router-link>
    </li>
    <li class="nav-item" v-for="room in allRooms" :key="room.id">
      <router-link
        :to="{ name: 'Room', params: { id: room.id } }"
        class="nav-link active"
        >{{ room.name }}</router-link
      >
    </li>
  </ul>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "RoomSelector",
  methods: {
    ...mapActions(["retrieveRooms", "deleteRoom"]),
  },
  computed: {
    ...mapGetters(["allRooms"]),
  },
  created() {
    this.retrieveRooms();
  },
};
</script>
