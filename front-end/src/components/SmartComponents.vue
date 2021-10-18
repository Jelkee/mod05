<!-- v-for="component in getComponents(this.$route.params.id)" -->
<!-- :key="component.id" -->

<template>
  <div class="container-fluid">
    <p v-if="noComponents">This room has no components</p>
    <div
      class="card"
      style="width: 18rem;"
      v-for="component in getComponents(getRoomId)"
      :key="component.id"
    >
      <div class="card-body">
        <h5 class="card-title">{{ component.name }}</h5>
        <h6 class="card-subtitle mb-2 text-muted">
          {{ component.type }}
        </h6>
        <div class="form-check form-switch">
          <input
            class="form-check-input"
            type="checkbox"
            id="flexSwitchCheckDefault"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "SmartComponents",
  computed: {
    ...mapGetters(["getComponents", "allComponents"]),
    getRoomId: function() {
      return Number(this.$route.params.id);
    },
    noComponents: function() {
      return this.getComponents(this.getRoomId).length === 0;
    },
  },
  methods: {
    ...mapActions(["retrieveComponents"]),
  },
  created() {
    this.retrieveComponents();
  },
};
</script>
