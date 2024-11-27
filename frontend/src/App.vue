<script setup lang="ts">
import { ref } from "vue";
import TreeDiagram from "./components/TreeDiagram.vue";
import TreeList from "./components/TreeList.vue";

const selectedTreeId = ref("");

function handleTreeSelect(treeId) {
	selectedTreeId.value = treeId;
}
</script>

<template>
  <div class="app-container">
    <div class="tree-list-wrapper">
      <TreeList @tree-select="handleTreeSelect"/>
    </div>
    <div class="tree-wrapper" v-if="selectedTreeId">
      <TreeDiagram :treeId="selectedTreeId"/>
    </div>
  </div>
</template>

<style>
.app-container {
  display: flex;
  width: 100%;
  height: 100vh;
}
.tree-list-wrapper {
  width: 100%;
  border-right: 1px solid #ccc;
}
.tree-wrapper {
  flex: 1;
  display: flex;
}
html, body, #app {
  height: 100%;
  margin: 0;
}
</style>