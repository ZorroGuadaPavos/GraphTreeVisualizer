export type HTTPValidationError = {
	detail?: Array<ValidationError>;
};

export type NodePublic = {
	name: string;
	id: string;
	label: string;
};

export type TreePublic = {
	name: string;
	id: string;
	children?: Array<TreePublic> | null;
};

export type ValidationError = {
	loc: Array<string | number>;
	msg: string;
	type: string;
};
