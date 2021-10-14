<template>
  <router-view />
</template>

<script>
export default {
  name: "App",
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
