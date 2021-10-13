<template>
  <div>
    <p>Messages</p>
    <ul>
      <Message
        v-for="message in messages"
        :message="message"
        :key="message.id"
      />
    </ul>
  </div>
</template>

<script>
import Message from "./Message.vue";

export default {
  name: "Messages",
  props: { messages: Array },
  components: { Message },
};
</script>
