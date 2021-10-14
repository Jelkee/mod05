<template>
  <div>
    <p>Components:</p>
    <ul>
      <li v-for="smart_component in allComponents" :key="smart_component.id">
        {{ smart_component.name }} - {{ smart_component.type }}
      </li>
    </ul>
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
