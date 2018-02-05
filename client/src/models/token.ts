export class TokenModel {
  public token: string;
}

export class TokenStateSchema {
  user: string;
  token: string;
}

export const TokenEmptyState = {token: '', user: ''};
