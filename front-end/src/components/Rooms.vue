<template>
  <div>
    <p>Rooms:</p>
    <ul>
      <li v-for="room in allRooms" :key="room.id">
        {{ room.name }}
        <button @click="deleteRoom(room.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "Rooms",
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
