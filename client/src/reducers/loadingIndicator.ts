import { Action, Reducer } from 'redux';

import { AppState } from '../constants/types';
import { LoadingIndicatorEmptyState, LoadingIndicatorSchema } from '../models/loadingIndicator';
import { LoadingIndicatorActivityReducer } from './activityLogs';
import { LoadingIndicatorBuildReducer } from './builds';
import { LoadingIndicatorChartViewReducer } from './chartViews';
import { LoadingIndicatorCodeReferenceReducer } from './codeReferences';
import { LoadingIndicatorExperimentJobReducer } from './experimentJobs';
import { LoadingIndicatorExperimentReducer } from './experiments';
import { LoadingIndicatorGroupReducer } from './groups';
import { LoadingIndicatorHealthStatusReducer } from './healthStatus';
import { LoadingIndicatorJobReducer } from './jobs';
import { LoadingIndicatorK8SResourceReducer } from './k8sResources';
import { LoadingIndicatorMetricReducer } from './metrics';
import { LoadingIndicatorNotebooksReducer } from './notebooks';
import { LoadingIndicatorOptionsReducer } from './options';
import { LoadingIndicatorOutputsReducer } from './outputs';
import { LoadingIndicatorProjectReducer } from './projects';
import { LoadingIndicatorSearchesReducer } from './searches';
import { LoadingIndicatorStatusesReducer } from './statuses';
import { LoadingIndicatorStoreReducer } from './stores';
import { LoadingIndicatorTensorboardsReducer } from './tensorboards';

export const LoadingIndicatorReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: any) => {
    return state;
  };

export const LoadingIndicatorSliceReducer = (state: AppState, action: Action) => {
  let newState = LoadingIndicatorActivityReducer(state.loadingIndicators, action);
  newState = LoadingIndicatorHealthStatusReducer(newState, action);
  newState = LoadingIndicatorChartViewReducer(newState, action);
  newState = LoadingIndicatorOutputsReducer(newState, action);
  newState = LoadingIndicatorMetricReducer(newState, action);
  newState = LoadingIndicatorStatusesReducer(newState, action);
  newState = LoadingIndicatorSearchesReducer(newState, action);
  newState = LoadingIndicatorCodeReferenceReducer(newState, action);
  newState = LoadingIndicatorNotebooksReducer(newState, action);
  newState = LoadingIndicatorTensorboardsReducer(newState, action);
  newState = LoadingIndicatorBuildReducer(newState, action);
  newState = LoadingIndicatorExperimentJobReducer(newState, action);
  newState = LoadingIndicatorExperimentReducer(newState, action);
  newState = LoadingIndicatorGroupReducer(newState, action);
  newState = LoadingIndicatorJobReducer(newState, action);
  newState = LoadingIndicatorOptionsReducer(newState, action);
  newState = LoadingIndicatorK8SResourceReducer(newState, action);
  newState = LoadingIndicatorStoreReducer(newState, action);
  return LoadingIndicatorProjectReducer(newState , action);
};
