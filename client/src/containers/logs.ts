import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as actions from '../actions/logs';
import Logs from '../components/logs';
import { AppState } from '../constants/types';
import { downloadName, logsDownloadUrl } from '../utils/downloads';

export function mapStateToProps(state: AppState, params: any) {
  return {
    logs: state.logs,
    downloadLogsUrl: logsDownloadUrl(params.project, params.resource, params.id),
    downloadLogsName: downloadName(params.project, params.resource, params.id),
  };
}

export interface DispatchProps {
  fetchData?: () => actions.LogsAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.LogsAction>, params: any): DispatchProps {
  return {
    fetchData: () => dispatch(actions.fetchLogs(
      params.project, params.resource, params.id, params.subResource, params.sid))
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Logs);
