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
export default {
  name: "AddUser",
  methods: {
    onSubmit() {
      if (!this.room_name) {
        alert("Please select a name for the room");
      } else {
        this.$emit("add-room", this.room_name);
        this.room_name = "";
      }
    },
  },
};
</script>
