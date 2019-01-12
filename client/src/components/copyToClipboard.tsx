import * as React from 'react';

import * as copy from 'copy-to-clipboard';

export interface Props {
  text: string;
  children: any;
}

export default class CopyToClipboard extends React.Component<Props, {}> {
  public onClick = (event: any) => {
    const elem = React.Children.only(this.props.children);
    copy(this.props.text);

    // Bypass onClick if it was present
    if (elem && elem.props && typeof elem.props.onClick === 'function') {
      elem.props.onClick(event);
    }
  };

  public render() {
    const {
      text, children, ...props
    } = this.props;
    const elem = React.Children.only(children);

    return React.cloneElement(elem, {...props, onClick: this.onClick});
  }
}
