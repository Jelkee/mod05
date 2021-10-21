<template>
  <div>
    <p v-if="noComponents">This room has no components</p>
    <div
      class="card"
      style="width: 12rem;"
      v-for="component in getComponents(roomId)"
      :key="component.id"
    >
      <div
        class="card-header container-fluid"
        style="background: white; border-style: none;"
      >
        <div class="row">
          <div class="col-md-10">
            <i
              class="fas fa-lightbulb text-primary"
              style="font-size: 35px"
            ></i>
          </div>
          <div class="col-md-2 float-right">
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
      <div class="card-body">
        <h5 class="card-title">{{ component.name }}</h5>
        <h6 class="card-subtitle mb-2 text-muted">
          {{ component.type }}
        </h6>
      </div>
      <div class="card-footer" style="background-color: white;">
        <div class="row">
          <div class="col-md-10">
            Auto
          </div>
          <div class="col-md-2 float-right">
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
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "SmartComponents",
  computed: {
    ...mapGetters(["getComponents", "allComponents"]),
    roomId: function() {
      return Number(this.$route.params.id);
    },
    noComponents: function() {
      return this.getComponents(this.roomId).length === 0;
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
