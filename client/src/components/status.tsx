import * as React from 'react';
import './status.less';

export interface Props {
  status: string;
}

function Status({status}: Props) {
  let getCssClassForStatus = (): string => {
    if (status === 'succeeded') {
      return 'success';
    } else if (status === 'stopped') {
      return 'danger';
    } else if (status === 'failed') {
      return 'danger';
    } else if (status === 'created') {
      return 'info';
    }
    return 'running';
  };
  return (
    <span className={`status alert alert-${getCssClassForStatus()}`}>
      {status}
    </span>
  );
}

export default Status;
