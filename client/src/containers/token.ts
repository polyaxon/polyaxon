import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as actions from '../actions/user';
import Token from '../components/token';
import { AppState } from '../constants/types';

export function mapStateToProps(state: AppState, props: {})  {
  return {token: state.auth.token};
}

export interface DispatchProps {
  fetchUser?: () => actions.UserAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.UserAction>, props: {}): DispatchProps {
  return {
    fetchUser: () => dispatch(actions.fetchUser()),
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Token);
