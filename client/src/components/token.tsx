import * as React from 'react';

import * as actions from '../actions/user';

export interface Props {
  token: string;
  fetchUser: () => actions.UserAction;
}

export default class Token extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.fetchUser();
  }

  public render() {
    return (
      <div className="jumbotron jumbotron-action">
        Your token is: {this.props.token}
      </div>
    );
  }
}
