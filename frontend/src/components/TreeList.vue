<template>
  <h2>Tree List</h2>
  <ul class="tree-list">
    <li v-for="id in treeIds" :key="id" @click="selectTree(id)">
      {{ id }}
    </li>
  </ul>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      treeIds: [],
      apiUrl: "http://127.0.0.1:8000/api/v1/trees/",
    };
  },
  mounted() {
    this.fetchTreeIds();
  },
  methods: {
    fetchTreeIds() {
      axios
        .get(this.apiUrl)
        .then((response) => {
          this.treeIds = response.data;
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