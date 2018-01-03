import * as React from "react";
import * as _ from "lodash";
import {Button, ButtonToolbar, FormGroup, FormControl, ControlLabel, HelpBlock} from "react-bootstrap";
import * as Cookies from 'js-cookie';

import {ProjectModel} from "../models/project";
import Experiments from "../containers/experiments";
import Groups from "../containers/groups";


export interface Props {
  fetchToken: (username: string, password: string) => any;
  history: any;
}


export default class Login extends React.Component<Props, Object> {
  componentDidMount() {
    const {fetchToken, history} = this.props;
  }
  
  public handleSubmit(event: any) {
    event.preventDefault();
    let username = (document.getElementById('username') as HTMLInputElement).value;
    let password = (document.getElementById('password') as HTMLInputElement).value;
    
    this.props.fetchToken(username, password).then((resp: any) => {
      Cookies.set('token', resp.token.token);
      Cookies.set('user', resp.username);
      this.props.history.push( `/${username}/`);
    }).catch((err: string) => {
      (document.getElementById('error-message') as HTMLElement).innerHTML = 'Unable to log in with provided credentials.';
    });
  }
  
  public render () {
    return (
      <form className="form" onSubmit={this.handleSubmit.bind(this)}>
          <div>
              <label>Username:</label>
              <input type="text" id="username"/>
          </div>
          <div>
              <label>Password:</label>
              <input type="password" id="password" />
          </div>
          <div className="submit">
              <input type="submit" value="Submit" className="button btn btn-polyaxon" />
          </div>
          <div className="error-message red" id="error-message"></div>
      </form>
    )
  }

}
