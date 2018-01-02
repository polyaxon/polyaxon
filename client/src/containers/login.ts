import { connect, Dispatch } from "react-redux";
import * as _ from "lodash";
import {withRouter} from "react-router-dom";

import { AppState } from "../constants/types";

import * as actions from "../actions/token";
import Login from "../components/login"


export function mapStateToProps(state: AppState, params: any)  {
  return {}
}

export interface DispatchProps {
  fetchToken?: (username: string, password: string) => any;
}


export function mapDispatchToProps(dispatch: Dispatch<actions.TokenAction>, params: any): DispatchProps {
  return {
    fetchToken: (username: string, password: string) => dispatch(actions.fetchToken(username, password))
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Login));