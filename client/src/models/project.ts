export class ProjectModel {
	public uuid: string;
	public name: string;
	public user: string;
	public num_experiments: number;
	public unique_name: string;
	public is_public: boolean;
	public deleted?: boolean;
	public description?: string;
	public isPrivate?: boolean = false;
	public createdAt: Date;
	public updatedAt: Date;
}

export class ProjectStateSchema {
	byUuids: {[uuid: string]: ProjectModel};
	uuids: string[];
}

export const ProjectsEmptyState = {byUuids: {}, uuids: []};
