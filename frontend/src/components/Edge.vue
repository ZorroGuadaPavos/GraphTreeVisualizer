<template>
  <path
    class="link"
    :d="path"
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
.link {
  fill: none;
  stroke: #d1d1d1;
  stroke-width: 2px;
}
</style>