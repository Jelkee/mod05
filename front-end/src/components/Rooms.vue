<template>
  <div>
    <p>Rooms:</p>
    <ul>
      <Room
        v-for="room in rooms"
        :key="room.id"
        :room="room"
        @delete-room="onDeleteRoom"
      ></Room>
    </ul>
  </div>
</template>

<script>
import Room from "./Room.vue";

export default {
  name: "Rooms",
  props: {
    rooms: Array,
  },
  components: { Room },
  methods: {
    onDeleteRoom(id) {
      this.$emit("delete-room", id);
    },
  },
};
</script>
