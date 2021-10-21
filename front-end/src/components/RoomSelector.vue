<template>
  <ul class="nav">
    <li class="nav-item" v-for="room in allRooms" :key="room.id">
      <router-link
        :to="{ name: 'Room', params: { id: room.id } }"
        class="nav-link"
        :class="{ active: isActive(room.id) }"
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
    isActive(id) {
      return id === this.roomId;
    },
  },
  computed: {
    ...mapGetters(["allRooms"]),
    roomId: function() {
      return Number(this.$route.params.id);
    },
  },
  created() {
    this.retrieveRooms();
  },
};
</script>
