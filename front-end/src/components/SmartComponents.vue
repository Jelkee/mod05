<template>
  <div>
    <p>Components:</p>
    <ul>
      <SmartComponent
        v-for="smart_component in smart_components"
        :key="smart_component.id"
        :smart_component="smart_component"
      />
    </ul>
  </div>
</template>

<script>
import SmartComponent from "./SmartComponent.vue";

export default {
  name: "SmartComponents",
  props: { smart_components: Array },
  components: { SmartComponent },
};
</script>
