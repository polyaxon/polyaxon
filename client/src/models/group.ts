export class GroupModel {
  public uuid: string;
  public unique_name: string;
  public description: string;
  public id: number;
  public num_experiments: number;
  public project_name: string;
  public user: string;
  public concurrency: number;
  public content: string;
  public tags: Array<string> = [];
  public num_scheduled_experiments?: number;
  public num_pending_experiments?: number;
  public num_running_experiments?: number;
  public num_succeeded_experiments?: number;
  public num_failed_experiments?: number;
  public num_stopped_experiments?: number;
  public deleted?: boolean;
  public created_at: string;
  public updated_at: string;
  public started_at: string;
  public finished_at: string;
  public last_status: string;
  public current_iteration: number;
  public search_algorithm: string;
  public experiments: Array<string> = [];
}

export class GroupStateSchema {
  byUniqueNames: {[uniqueName: string]: GroupModel};
  uniqueNames: string[];
}

export const GroupsEmptyState = {byUniqueNames: {}, uniqueNames: []};
