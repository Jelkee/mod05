<template>
  <div id="wrapper">
    <SideBar />

    <div id="content-wrapper" class="d-flex flex-column">
      <div id="content">
        <TopBar />
        <div class="container-fluid">
          <RoomSelector />
          <SmartComponents />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RoomSelector from "../components/RoomSelector.vue";
import SmartComponents from "../components/SmartComponents.vue";
import SideBar from "../components/layout/SideBar.vue";
import TopBar from "../components/layout/TopBar.vue";

export default {
  name: "Dashboard",
  components: { RoomSelector, SmartComponents, SideBar, TopBar },
};
</script>
