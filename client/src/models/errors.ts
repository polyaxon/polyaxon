export class ErrorEntityModel {
  public byIds: { [id: string]: { error: any, type: string } };
  public global: { [type: string]: any };
}

export const ErrorEntityEmpty = () => ({
  byIds: {},
  global: {},
});

export class ErrorSchema {
  public projects: ErrorEntityModel;
  public groups: ErrorEntityModel;
  public experiments: ErrorEntityModel;
  public experimentJobs: ErrorEntityModel;
  public jobs: ErrorEntityModel;
  public notebooks: ErrorEntityModel;
  public tensorboards: ErrorEntityModel;
  public builds: ErrorEntityModel;
  public metrics: ErrorEntityModel;
  public statuses: ErrorEntityModel;
  public outputs: ErrorEntityModel;
  public chartViews: ErrorEntityModel;
  public searches: ErrorEntityModel;
  public activityLogs: ErrorEntityModel;
  public healthStatus: ErrorEntityModel;
  public codeReference: ErrorEntityModel;
}

export const ErrorEmptyState = {
  projects: ErrorEntityEmpty(),
  groups: ErrorEntityEmpty(),
  experiments: ErrorEntityEmpty(),
  experimentJobs: ErrorEntityEmpty(),
  jobs: ErrorEntityEmpty(),
  notebooks: ErrorEntityEmpty(),
  tensorboards: ErrorEntityEmpty(),
  builds: ErrorEntityEmpty(),
  metrics: ErrorEntityEmpty(),
  statuses: ErrorEntityEmpty(),
  outputs: ErrorEntityEmpty(),
  chartViews: ErrorEntityEmpty(),
  searches: ErrorEntityEmpty(),
  activityLogs: ErrorEntityEmpty(),
  healthStatus: ErrorEntityEmpty(),
  codeReference: ErrorEntityEmpty(),
};

export const processErrorById = (state: ErrorEntityModel,
                                 id: number | string,
                                 error: any,
                                 type: string) => {
  const idState: { [id: string]: { error: any, type: string } } = {};
  idState[id.toString()] = {type, error};
  return {
    ...state,
    byIds: {...state.byIds, ...idState}
  };
};

export const processErrorGlobal = (state: ErrorEntityModel,
                                   error: any,
                                   type: string) => {
  const newState: { [type: string]: any } = {};
  newState[type] = error;
  return {
    ...state,
    global: {...state.global, ...newState}
  };
};
