<template>
  <g :transform="`translate(${position.y},${position.x})`" @click="handleClick">
    <rect
      :width="width"
      :height="height"
      :x="-width / 2"
      :y="-height / 2"
      rx="8"
      ry="8"
      style="fill: #f7f7f7; stroke: #333; stroke-width: 1.5px;"
    ></rect>
    <text
      dy=".35em"
      text-anchor="middle"
      style="font-size: 14px; fill: #333;"
    >
      {{ data.name }}
    </text>
  </g>
</template>

<script>
export default {
  props: {
    data: Object,
    position: Object,
    width: {
      type: Number,
      default: 80,
    },
    height: {
      type: Number,
      default: 30,
    },
  },
  methods: {
    handleClick() {
      this.$emit('node-clicked', { nodeId: this.data.id });
    },
  },
};
</script>

<style scoped>
/* ...existing styles... */
</style>