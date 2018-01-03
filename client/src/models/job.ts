export class JobModel {
	public uuid: string;
	public unique_name: string;
	public sequence: number;
	public role: string;
	public last_status: string;
	public experiment_name: string;
	public experiment: string;
	public definition: string;
	public deleted?: boolean;
	public project?: string;
	public status?: string;
	public createdAt: Date;
	public updatedAt: Date;
	public started_at: Date;
	public finished_at: Date;
}

export class JobStateSchema {
	byUuids: {[uuid: string]: JobModel};
	uuids: string[];
}

export const JobsEmptyState = {byUuids: {}, uuids: []};
