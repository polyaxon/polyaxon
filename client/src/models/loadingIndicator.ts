export class LoadingIndicatorEntityModel {
  public byIds: { [id: string]: { isLoading: boolean, type: string } };
  public global: { [type: string]: boolean};
}

export const getLoadingIndicatorEntityEmpty = () => ({
  byIds: {},
  global: {},
});

export class LoadingIndicatorSchema {
  public projects: LoadingIndicatorEntityModel;
  public groups: LoadingIndicatorEntityModel;
  public experiments: LoadingIndicatorEntityModel;
  public experimentJobs: LoadingIndicatorEntityModel;
  public jobs: LoadingIndicatorEntityModel;
  public notebooks: LoadingIndicatorEntityModel;
  public tensorboards: LoadingIndicatorEntityModel;
  public builds: LoadingIndicatorEntityModel;
  public metrics: LoadingIndicatorEntityModel;
  public statuses: LoadingIndicatorEntityModel;
  public outputs: LoadingIndicatorEntityModel;
  public chartViews: LoadingIndicatorEntityModel;
  public searches: LoadingIndicatorEntityModel;
  public activityLogs: LoadingIndicatorEntityModel;
  public healthStatus: LoadingIndicatorEntityModel;
  public codeReference: LoadingIndicatorEntityModel;
  public options: LoadingIndicatorEntityModel;
  public k8sResources: LoadingIndicatorEntityModel;
  public stores: LoadingIndicatorEntityModel;
  public accesses: LoadingIndicatorEntityModel;
}

export const LoadingIndicatorEmptyState = {
  projects: getLoadingIndicatorEntityEmpty(),
  groups: getLoadingIndicatorEntityEmpty(),
  experiments: getLoadingIndicatorEntityEmpty(),
  experimentJobs: getLoadingIndicatorEntityEmpty(),
  jobs: getLoadingIndicatorEntityEmpty(),
  notebooks: getLoadingIndicatorEntityEmpty(),
  tensorboards: getLoadingIndicatorEntityEmpty(),
  builds: getLoadingIndicatorEntityEmpty(),
  metrics: getLoadingIndicatorEntityEmpty(),
  statuses: getLoadingIndicatorEntityEmpty(),
  outputs: getLoadingIndicatorEntityEmpty(),
  chartViews: getLoadingIndicatorEntityEmpty(),
  searches: getLoadingIndicatorEntityEmpty(),
  activityLogs: getLoadingIndicatorEntityEmpty(),
  healthStatus: getLoadingIndicatorEntityEmpty(),
  codeReference: getLoadingIndicatorEntityEmpty(),
  options: getLoadingIndicatorEntityEmpty(),
  k8sResources: getLoadingIndicatorEntityEmpty(),
  stores: getLoadingIndicatorEntityEmpty(),
  accesses: getLoadingIndicatorEntityEmpty(),
};

export const processLoadingIndicatorById = (state: LoadingIndicatorEntityModel,
                                            id: number | string,
                                            isLoading: boolean,
                                            type: string) => {
  const idState: { [id: string]: { isLoading: boolean, type: string } } = {};
  idState[id.toString()] = {type, isLoading};
  return {
    ...state,
    byIds: {...state.byIds, ...idState}
  };
};

export const processLoadingIndicatorGlobal = (state: LoadingIndicatorEntityModel,
                                              isLoading: boolean,
                                              type: string) => {
  const newState: { [type: string]: boolean} = {};
  newState[type] = isLoading;
  return {
    ...state,
    global: {...state.global, ...newState}
  };
};

export const initLoadingIndicatorById = (state: LoadingIndicatorEntityModel,
                                         id: number | string) => {
  const idState: { [id: string]: any } = {};
  idState[id.toString()] = {};
  return {
    ...state,
    byIds: {...state.byIds, ...idState}
  };
};

export const initLoadingIndicator = (state: LoadingIndicatorEntityModel) => {
  return {
    ...state,
    global: {}
  };
};
