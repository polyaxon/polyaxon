import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import { AppState } from '../constants/types';
import { StatusModel } from '../models/status';

import * as actions from '../actions/statuses';
import Statuses from '../components/statuses';

export function mapStateToProps(state: AppState, params: any) {
  let useLastFetched = () => {
    let statusIds = state.statuses.lastFetched.ids;
    let count = state.statuses.lastFetched.count;
    let statuses: StatusModel[] = [];
    statusIds.forEach(
      function (statusId: number, idx: number) {
        statuses.push(state.statuses.byIds[statusId]);
      });
    return {statuses: statuses, count: count};
  };
  let results = useLastFetched();

  return {
    statuses: results.statuses,
    count: results.count
  };
}

export interface DispatchProps {
  fetchData?: () => actions.StatusesAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.StatusesAction>, params: any): DispatchProps {
  return {
    fetchData: () => {
      return dispatch(actions.fetchStatuses(params.project, params.resource, params.id));
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Statuses);
