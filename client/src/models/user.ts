export class UserModel {
  public username: string;
  public email: string;
  public isSuperuser: boolean;
  public num_projects: number;
  public projects: string[] = [];
}

export class UserStateSchema {
  public byUserNames: { [username: string]: UserModel };
  public userNames: string[];
}

export const UserEmptyState = {byUserNames: {}, userNames: []};
