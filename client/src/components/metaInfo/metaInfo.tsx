import * as React from 'react';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';

import './metaInfo.less';

export interface Props {
  icon: string;
  name: string;
  value: string|number|boolean|React.ReactNode;
  tooltip?: string;
  inline?: boolean;
  extraClass?: string;
}

function MetaInfo({icon, name, value, tooltip, inline = false, extraClass = ''}: Props) {
  const tooltipContent = (
    <Tooltip id="tooltipId">
      {tooltip}
    </Tooltip>
  );

  function getInfo() {
    const info = (
      <span className={`meta-info ${extraClass}`}>
        <i className={`fa ${icon} icon`} aria-hidden="true"/>
        <span className="title">{name}:</span>
        {value}
      </span>
    );
    return tooltip ? (
      <OverlayTrigger placement="bottom" overlay={tooltipContent}>
      {info}
      </OverlayTrigger>
    ) : info;
  }

  function getMetaInfo() {
    if (inline) {
      return (getInfo());
    }
    return (<div className="row meta">{getInfo()}</div>);
  }

  return (getMetaInfo());
}

export default MetaInfo;
