import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import { AppState } from '../constants/types';

import * as actions from '../actions/activityLog';
import { ActivityLogModel } from '../models/activitylog';
import ActivityLogs from '../components/activityLogs';

interface OwnProps {
  user?: string;
  projectName?: string;
  history?: boolean;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, ownProps: OwnProps) {
  let useLastFetched = () => {
    let activityLogIds = state.activityLogs.lastFetched.ids;
    let count = state.activityLogs.lastFetched.count;
    let activityLogs: ActivityLogModel[] = [];
    activityLogIds.forEach(
      function (activityLogId: number, idx: number) {
        activityLogs.push(state.activityLogs.byIds[activityLogId]);
      });
    return {activityLogs: activityLogs, count: count};
  };
  let results = useLastFetched();

  return {
    isCurrentUser: state.auth.user === ownProps.user,
    activityLogs: results.activityLogs,
    count: results.count,
  };
}

export interface DispatchProps {
  fetchData?: (offset?: number) => actions.ActivityLogAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ActivityLogAction>, ownProps: OwnProps): DispatchProps {
  return {
    fetchData: (offset?: number) => {
      let filters: {[key: string]: number|boolean|string} = {};
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
