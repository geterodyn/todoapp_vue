<template>
  <div>
    <b-alert variant="success" show fade dismissible>{{ message }}</b-alert>
  </div>
</template>

<script>
export default {
  props: ['message'],
};
</script>
