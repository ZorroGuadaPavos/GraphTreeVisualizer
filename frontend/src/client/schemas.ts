export const $HTTPValidationError = {
	properties: {
		detail: {
			type: "array",
			contains: {
				type: "ValidationError",
			},
		},
	},
} as const;

export const $NodePublic = {
	properties: {
		name: {
			type: "string",
			isRequired: true,
		},
		id: {
			type: "string",
			isRequired: true,
		},
		label: {
			type: "string",
			isRequired: true,
		},
	},
} as const;

export const $TreePublic = {
	properties: {
		name: {
			type: "string",
			isRequired: true,
		},
		id: {
			type: "string",
			isRequired: true,
		},
		children: {
			type: "any-of",
			contains: [
				{
					type: "array",
					contains: {
						type: "TreePublic",
					},
				},
				{
					type: "null",
				},
			],
		},
	},
} as const;

export const $ValidationError = {
	properties: {
		loc: {
			type: "array",
			contains: {
				type: "any-of",
				contains: [
					{
						type: "string",
					},
					{
						type: "number",
					},
				],
			},
			isRequired: true,
		},
		msg: {
			type: "string",
			isRequired: true,
		},
		type: {
			type: "string",
			isRequired: true,
		},
	},
} as const;
