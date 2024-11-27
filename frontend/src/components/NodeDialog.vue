<template>
  <div v-if="visible" class="dialog-overlay">
    <div class="dialog">
      <h2 class="header-title">Node: {{ nodeData.name }}</h2>
      <div class="node-details">
        <p><span class="bold-label">ID:</span> {{ nodeData.id }}</p>
        <p><span class="bold-label">Label:</span> {{ nodeData.label }}</p>
      </div>
      <button @click="close">Close</button>
    </div>
  </div>
</template>

<script>
export default {
	props: {
		visible: Boolean,
		nodeData: Object,
	},
	methods: {
		close() {
			this.$emit("close");
		},
	},
};
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}
.dialog {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border-radius: 8px;
}
.dialog {
  color: grey;
}
.bold-label {
  font-weight: bold;
}
.header-title {
  color: black;
}
</style>