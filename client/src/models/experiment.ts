export class ExperimentModel {
	public uuid: string;
	public unique_name: string;
	public sequence: number;
	public description: string;
	public experiment_group_name: string;
	public user: string;
	public content: string;
	public num_jobs: number;
	public last_status: string;
	public project_name: string;
	public experiment_group: string;
	public deleted?: boolean;
	public project: string;
	public created_at: string;
	public updated_at: string;
	public started_at: string;
	public finished_at: string;
	public last_metric: {[metric: string]: number};
}

export class ExperimentStateSchema {
	byUuids: {[uuid: string]: ExperimentModel};
	uuids: string[];
}

export const ExperimentsEmptyState = {byUuids: {}, uuids: []};
