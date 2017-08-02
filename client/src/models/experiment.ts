export class ExperimentModel {
	public id: number;
	public name: string;
	public description: string;
  public project: number;
  public status: string;

	onCreate?: () => void;
  onDelete?: () => void;
	onUpdate?: () => void;
}
