export class ExperimentModel {
	public uuid: string;
	public name: string;
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
