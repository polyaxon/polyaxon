import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import { AppState } from '../constants/types';

import * as actions from '../actions/activityLog';
import ActivityLogs from '../components/activitylogs/activityLogs';
import { ACTIONS } from '../constants/actions';
import { isTrue } from '../constants/utils';
import { ActivityLogModel } from '../models/activitylog';
import { getErrorsGlobal } from '../utils/errors';

interface Props {
  user?: string;
  projectName?: string;
  history?: boolean;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, props: Props) {
  const useLastFetched = () => {
    const activityLogIds = state.activityLogs.lastFetched.ids;
    const count = state.activityLogs.lastFetched.count;
    const activityLogs: ActivityLogModel[] = [];
    activityLogIds.forEach(
      (activityLogId: number, idx: number) => {
        activityLogs.push(state.activityLogs.byIds[activityLogId]);
      });
    return {activityLogs, count};
  };
  const results = useLastFetched();

  const isLoading = isTrue(state.loadingIndicators.statuses.global.fetch);
  return {
    isCurrentUser: state.auth.user === props.user,
    activityLogs: results.activityLogs,
    count: results.count,
    isLoading,
    errors: getErrorsGlobal(state.alerts.statuses.global, isLoading, ACTIONS.FETCH),
  };
}

export interface DispatchProps {
  fetchData?: (offset?: number) => actions.ActivityLogAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ActivityLogAction>, props: Props): DispatchProps {
  return {
    fetchData: (offset?: number) => {
      const filters: { [key: string]: number | boolean | string } = {};
      if (offset) {
        filters.offset = offset;
      }
      if (props.history) {
        return dispatch(actions.fetchHistoryLogs(filters));
      } else if (props.projectName && props.user) {
        return dispatch(actions.fetchProjectActivityLogs(
          props.user,
          props.projectName,
          filters));
      } else {
        return dispatch(actions.fetchActivityLogs(filters));
      }
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(ActivityLogs);
