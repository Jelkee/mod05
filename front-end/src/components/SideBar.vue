<template>
  <!-- Sidebar -->
  <ul class="navbar-nav sidebar accordion" id="accordionSidebar">
    <!-- Sidebar - Brand -->
    <a
      class="sidebar-brand d-flex align-items-center justify-content-center"
      href="#"
    >
      <div class="sidebar-brand-icon">
        <i class="fas fa-home"></i>
      </div>
      <div class="sidebar-brand-text mx-1">Raspberry Home</div>
    </a>

    <!-- Nav Item - Dashboard -->
    <li class="nav-item active">
      <a class="nav-link" href="#">
        <i class="fas fa-fw fa-tachometer-alt"></i>
        <span>Dashboard</span></a
      >
    </li>

    <!-- Nav Item - Users -->
    <li class="nav-item">
      <a class="nav-link" href="#">
        <i class="fas fa-users"></i>
        <span>Users</span></a
      >
    </li>
  </ul>
  <!-- End of Sidebar -->
</template>

<script>
export default {
  name: "SideBar",
};
</script>
