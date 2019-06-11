import { Action, Reducer } from 'redux';

import { AppState } from '../constants/types';
import { AlertEmptyState, AlertSchema } from '../models/alerts';
import { AlertBuildReducer } from './builds';
import { AlertChartViewReducer } from './chartViews';
import { AlertCodeReferenceReducer } from './codeReferences';
import { AlertExperimentJobReducer } from './experimentJobs';
import { AlertExperimentReducer } from './experiments';
import { AlertGroupReducer } from './groups';
import { AlertHealthStatusReducer } from './healthStatus';
import { AlertJobReducer } from './jobs';
import { AlertMetricReducer } from './metrics';
import { AlertNotebooksReducer } from './notebooks';
import { AlertOptionsReducer } from './options';
import { AlertOutputsReducer } from './outputs';
import { AlertProjectReducer } from './projects';
import { AlertSearchesReducer } from './searches';
import { AlertStatusesReducer } from './statuses';
import { AlertTensorboardsReducer } from './tensorboards';

export const AlertReducer: Reducer<AlertSchema> =
  (state: AlertSchema = AlertEmptyState, action: any) => {
    return state;
  };

export const AlertSliceReducer = (state: AppState, action: Action) => {
  let newState = AlertReducer(state.alerts, action);
  newState = AlertHealthStatusReducer(newState, action);
  newState = AlertChartViewReducer(newState, action);
  newState = AlertOutputsReducer(newState, action);
  newState = AlertMetricReducer(newState, action);
  newState = AlertStatusesReducer(newState, action);
  newState = AlertSearchesReducer(newState, action);
  newState = AlertCodeReferenceReducer(newState, action);
  newState = AlertNotebooksReducer(newState, action);
  newState = AlertTensorboardsReducer(newState, action);
  newState = AlertBuildReducer(newState, action);
  newState = AlertExperimentJobReducer(newState, action);
  newState = AlertExperimentReducer(newState, action);
  newState = AlertGroupReducer(newState, action);
  newState = AlertJobReducer(newState, action);
  newState = AlertOptionsReducer(newState, action);
  return AlertProjectReducer(newState , action);
};
