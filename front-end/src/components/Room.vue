<template>
  <li>{{ room.name }}</li>
</template>

<script>
export default { name: "Room", props: { room: Object } };
</script>
