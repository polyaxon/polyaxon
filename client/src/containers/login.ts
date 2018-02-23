import { connect, Dispatch } from 'react-redux';
import { withRouter } from 'react-router-dom';

import { AppState } from '../constants/types';

import * as actions from '../actions/token';
import Login from '../components/login';

export function mapStateToProps(state: AppState, params: any)  {
  return {};
}

export interface DispatchProps {
  login?: (username: string, password: string) => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.TokenAction>, params: any): DispatchProps {
  return {
    login: (username: string, password: string) => dispatch(actions.login(username, password))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Login));
