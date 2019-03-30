import * as React from 'react';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';

import { CREATED, DONE, FAILED, STOPPED, SUCCEEDED, WARNING } from '../../constants/statuses';

import './status.less';

export interface Props {
  status: string;
  reducedForm?: boolean;
}

function Status({status, reducedForm}: Props) {
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
    } else if (status === WARNING) {
      return 'warning';
    }
    return 'running';
  };

  const getReducedStatus = () => {
    const tooltipContent = (
      <Tooltip id="tooltipId">
        {status}
      </Tooltip>
    );

    let icon: React.ReactNode;
    if (status === DONE) {
      icon = <i className="fas fa-check fa-sm icon" aria-hidden="true"/>;
    } else if (status === SUCCEEDED) {
      icon = <i className="fas fa-check fa-sm icon" aria-hidden="true"/>;
    } else if (status === STOPPED) {
      icon = <i className="fas fa-stop fa-sm icon" aria-hidden="true"/>;
    } else if (status === FAILED) {
      icon = <i className="fas fa-times fa-sm icon" aria-hidden="true"/>;
    } else if (status === CREATED) {
      icon = <i className="fas fa-pause fa-sm icon" aria-hidden="true"/>;
    } else if (status === WARNING) {
      icon = <i className="fas fa-exclamation fa-sm icon" aria-hidden="true"/>;
    } else {
      icon = <i className="fas fa-spinner fa-sm fa-spin icon" aria-hidden="true"/>;
    }
    return (
      <OverlayTrigger placement="bottom" overlay={tooltipContent}>
        {icon}
      </OverlayTrigger>
    );
  };
  const reducedClass = reducedForm ? 'alert-reduced' : '';
  return (
    <span className={`status alert alert-${getCssClassForStatus()} ${reducedClass}`}>
      {reducedForm ? getReducedStatus() : status}
    </span>
  );
}

export default Status;
