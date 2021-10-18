<template>
  <div id="wrapper">
    <SideBar />

    <div id="content-wrapper" class="d-flex flex-column">
      <div id="content">
        <TopBar />
        <router-view />
      </div>
    </div>
  </div>
  <router-view />
</template>

<script>
import SideBar from "./components/SideBar.vue";
import TopBar from "./components/TopBar.vue";

export default {
  name: "App",
  components: { SideBar, TopBar },
  computed: {
    signed_in() {
      if (this.$route.path !== "/") {
        return true;
      } else {
        return false;
      }
    },
  },
};
</script>

<style></style>
