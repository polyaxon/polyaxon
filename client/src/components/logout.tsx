import * as React from 'react';

import { getLoginUrl } from '../constants/utils';
import { delay } from '../constants/utils';

export interface Props {
  logout: () => any;
  history: any;
}

export default class Logout extends React.Component<Props, Object> {
  componentDidMount() {
    this.props.logout().then(() => delay(1).then(() => {
        this.props.history.push(getLoginUrl());
    }));
  }

  public render() {
    return (<div/>);
  }
}
