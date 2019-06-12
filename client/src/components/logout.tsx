import * as React from 'react';

import { delay } from '../constants/utils';
import { getLoginUrl } from '../urls/utils';

export interface Props {
  logout: () => any;
  history: any;
}

export default class Logout extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.logout().then(() => delay(1).then(() => {
        this.props.history.push(getLoginUrl());
    }));
  }

  public render() {
    return (<div/>);
  }
}
