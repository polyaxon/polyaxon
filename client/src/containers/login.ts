import { connect, Dispatch } from 'react-redux';
import { withRouter } from 'react-router-dom';

import { AppState } from '../constants/types';

import * as actions from '../actions/token';
import * as userActions from '../actions/user';
import Login from '../components/login';

export function mapStateToProps(state: AppState, params: any)  {
  let next = new URLSearchParams(params.location.search).get('next');
  return {next: next, isLoggedIn: Boolean(state.auth.user) && Boolean(state.auth.token)};
}

export interface DispatchProps {
  fetchUser: () => any;
  login?: (username: string, password: string) => any;
  refreshSession: () => any;
}

export function mapDispatchToProps(
  dispatch: Dispatch<actions.TokenAction | userActions.UserAction>, params: any): DispatchProps {
  return {
    fetchUser: () => dispatch(userActions.fetchUser()),
    login: (username: string, password: string) => dispatch(actions.login(username, password)),
    refreshSession: () => dispatch(actions.refreshSession()),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Login));
