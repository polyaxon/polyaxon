import * as React from 'react';
import './metaInfo.less';

export interface Props {
  icon: string;
  name: string;
  value: string|number|boolean|React.ReactNode;
  inline?: boolean;
}

function MetaInfo({icon, name, value, inline = false}: Props) {
  function getInfo() {
    return (
      <span className="meta-info">
        <i className={`fa ${icon} icon`} aria-hidden="true"/>
        <span className="title">{name}:</span>
        {value}
      </span>
    );
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
