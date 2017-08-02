export class ProjectModel {
	public id: number;
	public name: string;
	public description: string;
	public isPrivate: boolean;

	onCreate?: () => void;
  onDelete?: () => void;
	onUpdate?: () => void;
}
