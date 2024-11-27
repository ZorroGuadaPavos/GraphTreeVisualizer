<template>
  <h2>Tree List</h2>
  <ul class="tree-list">
    <li v-for="id in treeIds" :key="id" @click="selectTree(id)">
      {{ id }}
    </li>
  </ul>
</template>

<script>
import { TreesService } from "../client/services";

export default {
	data() {
		return {
			treeIds: [],
		};
	},
	mounted() {
		this.fetchTreeIds();
	},
	methods: {
		fetchTreeIds() {
			TreesService.treesGetAllTreeIds()
				.then((response) => {
					this.treeIds = response;
					if (this.treeIds.length > 0) {
						this.selectTree(this.treeIds[0]);
					}
				})
				.catch((error) => {
					console.error("Error fetching tree IDs:", error);
				});
		},
		selectTree(id) {
			this.$emit("tree-select", id);
		},
	},
};
</script>

<style>
.tree-list {
  list-style-type: none;
  padding: 0;
}
.tree-list li {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  color: #bcbcbc;
}
.tree-list li:hover {
  background-color: #525151;
}
</style>