import type { CancelablePromise } from "./core/CancelablePromise";
import { OpenAPI } from "./core/OpenAPI";
import { request as __request } from "./core/request";

import type { NodePublic, TreePublic } from "./models";

export type TreesData = {
	TreesReadTree: {
		treeId: string;
	};
	TreesReadNode: {
		nodeId: string;
		treeId: string;
	};
};

export class TreesService {
	/**
	 * Get All Tree Ids
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public static treesGetAllTreeIds(): CancelablePromise<Array<string>> {
		return __request(OpenAPI, {
			method: "GET",
			url: "/api/v1/trees/",
		});
	}

	/**
	 * Read Tree
	 * @returns TreePublic Successful Response
	 * @throws ApiError
	 */
	public static treesReadTree(
		data: TreesData["TreesReadTree"],
	): CancelablePromise<TreePublic> {
		const { treeId } = data;
		return __request(OpenAPI, {
			method: "GET",
			url: "/api/v1/trees/{tree_id}",
			path: {
				tree_id: treeId,
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Read Node
	 * @returns NodePublic Successful Response
	 * @throws ApiError
	 */
	public static treesReadNode(
		data: TreesData["TreesReadNode"],
	): CancelablePromise<NodePublic> {
		const { treeId, nodeId } = data;
		return __request(OpenAPI, {
			method: "GET",
			url: "/api/v1/trees/{tree_id}/nodes/{node_id}",
			path: {
				tree_id: treeId,
				node_id: nodeId,
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}
}
