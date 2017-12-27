export class ExperimentModel {
	public uuid: string;
	public unique_name: string;
	public sequence: number;
	public experiment_group_name: string;
	public user: string;
	public content: string;
	public project_name: string;
	public deleted?: boolean;
    public project?: string;
    public status?: string;
	public createdAt: Date;
	public updatedAt: Date;
}

export class ExperimentStateSchema {
	byUuids: {[uuid: string]: ExperimentModel};
	uuids: string[];
}

export const ExperimentsEmptyState = {byUuids: {}, uuids: []};
