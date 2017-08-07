export class ProjectModel {
	public id: number;
	public name: string;
	public description?: string;
	public isPrivate?: boolean = false;
	public experiments?: Array<number> = [];
}
