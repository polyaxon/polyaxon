import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import { AppState } from '../constants/types';

import * as actions from '../actions/activityLog';
import ActivityLogs from '../components/activitylogs/activityLogs';
import { isTrue } from '../constants/utils';
import { ActivityLogModel } from '../models/activitylog';

interface OwnProps {
  user?: string;
  projectName?: string;
  history?: boolean;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, ownProps: OwnProps) {
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

  return {
    isCurrentUser: state.auth.user === ownProps.user,
    activityLogs: results.activityLogs,
    count: results.count,
    isLoading: isTrue(state.loadingIndicators.statuses.global.fetch),
    errors: state.errors.statuses.global.fetch,
  };
}

export interface DispatchProps {
  fetchData?: (offset?: number) => actions.ActivityLogAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ActivityLogAction>, ownProps: OwnProps): DispatchProps {
  return {
    fetchData: (offset?: number) => {
      const filters: { [key: string]: number | boolean | string } = {};
      if (offset) {
        filters.offset = offset;
      }
      if (ownProps.history) {
        return dispatch(actions.fetchHistoryLogs(filters));
      } else if (ownProps.projectName && ownProps.user) {
        return dispatch(actions.fetchProjectActivityLogs(
          ownProps.user,
          ownProps.projectName,
          filters));
      } else {
        return dispatch(actions.fetchActivityLogs(filters));
      }
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(ActivityLogs);
