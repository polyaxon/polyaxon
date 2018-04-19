import { connect, Dispatch } from 'react-redux';

import { AppState } from '../constants/types';
import * as actions from '../actions/logs';
import Logs from '../components/logs';

export function mapStateToProps(state: AppState, params: any) {
  return {logs: state.logs}
}

export interface DispatchProps {
  fetchData?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.LogsAction>, params: any): DispatchProps {
  return {
    fetchData: () => dispatch(actions.fetchLogs('project-unique-name', 1))
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Logs);
