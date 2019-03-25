import { Action, Reducer } from 'redux';

import { AppState } from '../constants/types';
import { ErrorEmptyState, ErrorSchema } from '../models/errors';
import { ErrorBuildReducer } from './builds';
import { ErrorChartViewReducer } from './chartViews';
import { ErrorCodeReferenceReducer } from './codeReferences';
import { ErrorExperimentJobReducer } from './experimentJobs';
import { ErrorExperimentReducer } from './experiments';
import { ErrorGroupReducer } from './groups';
import { ErrorHealthStatusReducer } from './healthStatus';
import { ErrorJobReducer } from './jobs';
import { ErrorMetricReducer } from './metrics';
import { ErrorNotebooksReducer } from './notebooks';
import { ErrorOutputsReducer } from './outputs';
import { ErrorProjectReducer } from './projects';
import { ErrorSearchesReducer } from './searches';
import { ErrorStatusesReducer } from './statuses';
import { ErrorTensorboardsReducer } from './tensorboards';

export const ErrorReducer: Reducer<ErrorSchema> =
  (state: ErrorSchema = ErrorEmptyState, action: any) => {
    return state;
  };

export const ErrorSliceReducer = (state: AppState, action: Action) => {
  let newState = ErrorReducer(state.errors, action);
  newState = ErrorHealthStatusReducer(newState, action);
  newState = ErrorChartViewReducer(newState, action);
  newState = ErrorOutputsReducer(newState, action);
  newState = ErrorMetricReducer(newState, action);
  newState = ErrorStatusesReducer(newState, action);
  newState = ErrorSearchesReducer(newState, action);
  newState = ErrorCodeReferenceReducer(newState, action);
  newState = ErrorNotebooksReducer(newState, action);
  newState = ErrorTensorboardsReducer(newState, action);
  newState = ErrorBuildReducer(newState, action);
  newState = ErrorExperimentJobReducer(newState, action);
  newState = ErrorExperimentReducer(newState, action);
  newState = ErrorGroupReducer(newState, action);
  newState = ErrorJobReducer(newState, action);
  return ErrorProjectReducer(newState , action);
};
