export class UserModel {
  public username: string;
  public email: string;
  public isSuperuser: boolean;
}

export const UserEmptyState = {username: '', email: '', isSuperuser: false};
