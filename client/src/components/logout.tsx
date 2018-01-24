import * as React from "react";

import {getLoginUrl} from "../constants/utils";


export interface Props {
  discardToken: () => any;
  history: any;
}


export default class Logout extends React.Component<Props, Object> {
  componentDidMount() {
    const {discardToken, history} = this.props;
    discardToken();
    this.props.history.push(getLoginUrl());
  }

  public render() {
    return (<div></div>);
  }
}
