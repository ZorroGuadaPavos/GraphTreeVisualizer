<template>
  <path
    class="link"
    :d="path"
    style="fill: none; stroke: #d1d1d1; stroke-width: 2px;"
  ></path>
</template>

<script>
export default {
  props: {
    path: Object,
  },
};
</script>

<style scoped>
/* ...existing styles... */
</style>