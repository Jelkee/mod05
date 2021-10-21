<template>
  <div>
    <p>Messages:</p>
    <ul>
      <li v-for="message in allMessages" :key="message.id">
        {{ message.body }}
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "Messages",
  methods: {
    ...mapActions(["retrieveMessages"]),
  },
  computed: {
    ...mapGetters(["allMessages"]),
  },
  created() {
    this.retrieveMessages();
  },
};
</script>
