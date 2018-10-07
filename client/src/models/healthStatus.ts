export class TokenModel {
  public token: string;
  public csrftoken: string;
}

export class HealthStatusStateSchema {
  public status: { [key: string]: any };
}

export const HealthStatusEmptyState = {status: {}};
