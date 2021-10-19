<template>
  <div id="wrapper">
    <SideBar />

    <div id="content-wrapper" class="d-flex flex-column">
      <div id="content">
        <TopBar />
        <div class="container-fluid"></div>
      </div>
    </div>
  </div>
</template>

<script>
import SideBar from "../components/SideBar.vue";
import TopBar from "../components/TopBar.vue";

export default {
  name: "Components",
  components: { SideBar, TopBar },
};
</script>
