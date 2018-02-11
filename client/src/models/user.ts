export class UserModel {
  public username: string;
  public email: string;
  public isSuperuser: boolean;
  public num_projects: number;
  public projects: Array<string> = [];
}

export class UserStateSchema {
  byUserNames: {[username: string]: UserModel};
  userNames: string[];
}

export const UserEmptyState = {byUserNames: {}, userNames: []};
