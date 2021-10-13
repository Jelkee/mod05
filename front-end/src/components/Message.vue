<template>
  <li>{{ message.body }}</li>
</template>

<script>
export default {
  name: "Message",
  props: { message: Object },
};
</script>
