<template>
  <div>
    <p>Rooms:</p>
    <ul>
      <Room v-for="room in rooms" :key="room.id" :room="room"></Room>
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
};
</script>
