<template>
  <div id="wrapper">
    <SideBar />

    <div id="content-wrapper" class="d-flex flex-column">
      <div id="content">
        <TopBar />
        <RoomSelector />
        <SmartComponents />
      </div>
    </div>
  </div>
</template>

<script>
import SideBar from "../components/SideBar.vue";
import TopBar from "../components/TopBar.vue";
import RoomSelector from "../components/RoomSelector.vue";
import SmartComponents from "../components/SmartComponents.vue";

export default {
  name: "Dashboard",
  components: { SideBar, TopBar, RoomSelector, SmartComponents },
};
</script>
