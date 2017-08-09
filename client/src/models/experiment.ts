export class ExperimentModel {
	public id: number;
	public name: string;
  public project?: number;
  public status?: string;
	public createdAt: Date;
	public updatedAt: Date;
}

export class ExperimentStateSchema {
	byIds: {[id: number]: ExperimentModel};
	ids: number[];
}

export const ExperimentsEmptyState = {byIds: {}, ids: []};
