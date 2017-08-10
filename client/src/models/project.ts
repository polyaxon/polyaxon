export class ProjectModel {
	public id: number;
	public name: string;
	public deleted?: boolean;
	public description?: string;
	public isPrivate?: boolean = false;
	public experiments?: Array<number> = [];
	public createdAt: Date;
	public updatedAt: Date;
}

export class ProjectStateSchema {
	byIds: {[id: number]: ProjectModel};
	ids: number[];
}

export const ProjectsEmptyState = {byIds: {}, ids: []};
