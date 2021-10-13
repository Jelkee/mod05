<template>
  <li>
    {{ room.name }}
    <button @click="onDelete">Delete</button>
  </li>
</template>

<script>
export default {
  name: "Room",
  props: { room: Object },
  methods: {
    onDelete() {
      this.$emit("delete-room", this.room.id);
    },
  },
};
</script>
