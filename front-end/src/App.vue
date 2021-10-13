<template>
  <div>
    <SiteHeader />
    <Rooms :rooms="rooms" />
    <SmartComponents :smart_components="smart_components" />
  </div>
</template>

<script>
import SmartComponents from "./components/SmartComponents.vue";
import Rooms from "./components/Rooms.vue";
import SiteHeader from "./components/SiteHeader.vue";

const rooms = [
  { id: 0, name: "Living room" },
  { id: 1, name: "Kitchen" },
];

const smart_components = [
  { id: 0, roomID: 0, type: "light", name: "Light in living room" },
  {
    id: 1,
    roomID: 0,
    type: "light_sensor",
    name: "Light sensor in living room",
  },
  { id: 1, roomID: 1, type: "radiator", name: "Radiator in kitchen" },
];

export default {
  name: "App",
  components: { SiteHeader, Rooms, SmartComponents },
  data() {
    return { rooms, smart_components };
  },
};
</script>

<style></style>
