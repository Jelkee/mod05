<template>
  <div>
    <p>Users:</p>
    <ul>
      <li v-for="user in allUsers" :key="user.id">{{ user.name }}</li>
    </ul>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "Users",
  methods: {
    ...mapActions(["retrieveUsers"]),
  },
  computed: mapGetters(["allUsers"]),
  created() {
    this.retrieveUsers();
  },
};
</script>
