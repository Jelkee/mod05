<template>
  <SiteHeader />
  <router-view />
  <router-link to="/" v-if="signed_in">Sign out</router-link>
</template>

<script>
import SiteHeader from "./components/SiteHeader.vue";

export default {
  name: "App",
  components: { SiteHeader },
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
