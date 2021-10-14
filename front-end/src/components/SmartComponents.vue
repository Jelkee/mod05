<template>
  <div class="container-fluid">
    <div class="card" style="width: 18rem;">
      <div class="card-body">
        <h5 class="card-title">Light</h5>
        <h6 class="card-subtitle mb-2 text-muted">Living Room</h6>
        <a href="#" class="card-link">On/Off</a>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "SmartComponents",
  computed: {
    ...mapGetters(["allComponents"]),
  },
  methods: {
    ...mapActions(["retrieveComponents"]),
  },
  created() {
    this.retrieveComponents();
  },
};
</script>
