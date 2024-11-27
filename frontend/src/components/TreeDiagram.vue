<template>
  <div ref="treeContainer">
    <svg
      :width="width + margin.right + margin.left"
      :height="height + margin.top + margin.bottom"
    >
      <g :transform="`translate(${margin.left},${margin.top})`">
        <Edge
          v-for="(link, index) in links"
          :key="index"
          :path="generateLinkPath(link)"
        />
        <Node
          v-for="(node, index) in nodes"
          :key="index"
          :data="node.data"
          :position="{ x: node.x, y: node.y }"
          @node-clicked="handleNodeClick"
        />
      </g>
    </svg>
    <NodeDialog
      :visible="dialogVisible"
      :nodeData="dialogData"
      @close="closeDialog"
    />
  </div>
</template>

<script>
import * as d3 from "d3";
import Node from "./Node.vue";
import Edge from "./Edge.vue";
import NodeDialog from "./NodeDialog.vue";
import { TreesService } from "../client/services";

export default {
	props: {
		treeId: {
			type: String,
			required: true,
		},
	},
	components: {
		Node,
		Edge,
		NodeDialog,
	},
	data() {
		return {
			series: {},
			nodes: [],
			links: [],
			width: 800,
			height: 800,
			margin: { top: 25, right: 90, bottom: 30, left: 90 },
			dialogVisible: false,
			dialogData: null,
		};
	},
	watch: {
		treeId(newId) {
			this.fetchTreeData();
		},
	},
	mounted() {
		this.fetchTreeData();
	},
	methods: {
		fetchTreeData() {
			TreesService.treesReadTree({ treeId: this.treeId })
				.then((response) => {
					this.series = response;
					this.processTreeData();
				})
				.catch((error) => {
					console.error("Error fetching tree data:", error);
				});
		},
		processTreeData() {
			const treemap = d3.tree().size([this.height, this.width]);
			const root = d3.hierarchy(this.series);
			const treeData = treemap(root);
			this.nodes = treeData.descendants();
			this.links = treeData.links();
		},
		generateLinkPath(link) {
			return d3
				.linkHorizontal()
				.x((d) => d.y)
				.y((d) => d.x)(link);
		},
		handleNodeClick({ nodeId }) {
			TreesService.treesReadNode({ treeId: this.treeId, nodeId })
				.then((response) => {
					this.dialogData = response;
					this.dialogVisible = true;
				})
				.catch((error) => {
					console.error("Error fetching node data:", error);
				});
		},
		closeDialog() {
			this.dialogVisible = false;
			this.dialogData = null;
		},
	},
};
</script>

<style>
.link {
  fill: none;
  stroke: #d1d1d1;
  stroke-width: 2px;
}

.node rect {
  fill: #f7f7f7;
  stroke: #333;
  stroke-width: 1.5px;
}

.node text {
  font: 14px sans-serif;
  fill: #333;
}
</style>
