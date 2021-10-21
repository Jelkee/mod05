<template>
  <form @submit.prevent="onSubmit()">
    <div>
      <label>Username: </label>
      <input type="text" v-model="username" required />
      <input type="submit" value="Save" />
    </div>
  </form>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "AddUser",
  data() {
    return { username: "" };
  },
  methods: {
    ...mapActions(["addUser"]),
    onSubmit() {
      this.addUser(this.username);
    },
  },
};
</script>
