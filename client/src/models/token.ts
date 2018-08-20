export class TokenModel {
  public token: string;
  public csrftoken: string;
}

export class TokenStateSchema {
  public user: string;
  public token: string;
  public csrftoken: string;
}

export const TokenEmptyState = {token: '', user: '', csrftoken: ''};
