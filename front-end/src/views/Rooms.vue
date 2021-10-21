<template>
  <div id="wrapper">
    <!-- <SideBar /> -->

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
// import SideBar from "../components/layout/SideBar.vue";
import TopBar from "../components/layout/TopBar.vue";
import RoomsTable from "../components/tables/RoomsTable.vue";

export default {
  name: "Rooms",
  components: { RoomsTable, TopBar },
};
</script>
