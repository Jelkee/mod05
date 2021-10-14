<template>
  <ul class="nav">
    <li class="nav-item">
      <a class="nav-link active" href="#">Room 1</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="#">Room2</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="#">Room 3</a>
    </li>
  </ul>
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
