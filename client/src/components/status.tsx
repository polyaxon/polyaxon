import * as React from 'react';
import { CREATED, DONE, FAILED, STOPPED, SUCCEEDED } from '../constants/statuses';

import './status.less';

export interface Props {
  status: string;
}

function Status({status}: Props) {
  const getCssClassForStatus = (): string => {
    if (status === DONE) {
      return 'done';
    } else if (status === SUCCEEDED) {
      return 'success';
    } else if (status === STOPPED) {
      return 'danger';
    } else if (status === FAILED) {
      return 'danger';
    } else if (status === CREATED) {
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
