<template>
  <div>
    <h1>Raspberry Home</h1>
    <room-list></room-list>
  </div>
</template>

<script>
import RoomList from "./components/RoomList";

export default {
  name: "App",
  components: { RoomList },
};
</script>

<style></style>
