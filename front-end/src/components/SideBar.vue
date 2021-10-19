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
      <router-link to="/dashboard" class="nav-link">
        <i class="fas fa-fw fa-tachometer-alt"></i>
        <span>Dashboard</span></router-link
      >
    </li>

    <!-- Nav Item - Users -->
    <li class="nav-item">
      <router-link to="/users" class="nav-link">
        <i class="fas fa-users"></i>
        <span>Users</span></router-link
      >
    </li>

    <!-- Nav Item - Rooms -->
    <li class="nav-item">
      <router-link to="/rooms" class="nav-link">
        <i class="fas fa-chart-pie"></i>
        <span>Rooms</span></router-link
      >
    </li>

    <!-- Nav Item - Components -->
    <li class="nav-item">
      <router-link class="nav-link" to="/components">
        <i class="fas fa-puzzle-piece"></i>
        <span>Components</span></router-link
      >
    </li>

    <!-- Nav Item - Statistics -->
    <li class="nav-item">
      <a class="nav-link" href="#">
        <i class="fas fa-chart-pie"></i>
        <span>Statistics</span></a
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
