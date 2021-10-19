<template>
  <div id="wrapper">
    <SideBar />

    <div id="content-wrapper" class="d-flex flex-column">
      <div id="content">
        <TopBar />
        <div class="container-fluid">
          <RoomsTable />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SideBar from "../components/SideBar.vue";
import TopBar from "../components/TopBar.vue";
import RoomsTable from "../components/RoomsTable.vue";

export default {
  name: "Rooms",
  components: { RoomsTable, SideBar, TopBar },
};
</script>
