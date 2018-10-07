import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as actions from '../actions/healthStatus';
import HeathStatus from '../components/healthStatus';
import { AppState } from '../constants/types';

export function mapStateToProps(state: AppState, ownProps: any)  {
  return {healthStatus: state.healthStatus.status};
}

export interface DispatchProps {
  fetchData: () => actions.HealthStatusAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.HealthStatusAction>, params: any): DispatchProps {
  return {
    fetchData: () => dispatch(actions.fetchHealthStatus()),
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(HeathStatus);
