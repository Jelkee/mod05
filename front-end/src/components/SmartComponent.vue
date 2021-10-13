<template>
  <li>
    <div>
      <p>{{ smart_component.name }} - {{ smart_component.type }}</p>
    </div>
  </li>
</template>

<script>
export default {
  name: "SmartComponent",
  props: { smart_component: Object },
};
</script>
