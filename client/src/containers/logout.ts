import { connect, Dispatch } from 'react-redux';
import { withRouter } from 'react-router-dom';

import { AppState } from '../constants/types';
import * as actions from '../actions/token';
import Logout from '../components/logout';

export function mapStateToProps(state: AppState, params: any) {
  return {};
}

export interface DispatchProps {
  logout?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.TokenAction>, params: any): DispatchProps {
  return {
    logout: () => dispatch(actions.logout())
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Logout));
