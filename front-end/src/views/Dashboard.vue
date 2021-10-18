<template>
  <RoomSelector />
  <SmartComponents />
</template>

<script>
import RoomSelector from "../components/RoomSelector.vue";
import SmartComponents from "../components/SmartComponents.vue";

export default {
  name: "Dashboard",
  components: { RoomSelector, SmartComponents },
};
</script>
