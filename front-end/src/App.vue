<template>
  <q-layout view="lHh lpR lFf"> </q-layout>
</template>

<script>
import TopBar from "./components/TopBar.vue";
import MainPage from "./components/MainPage.vue";
import SideBar from "./components/SideBar.vue";
export default {
  name: "LayoutDefault",

  components: { SideBar, TopBar, MainPage },

  setup() {
    return {};
  },
};
</script>
