import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  icon: string;
  name: string;
  value: string;
  inline?: boolean;
}

function EntityMetaInfo({icon, name, value, inline = false}: Props) {
  return (
    <MetaInfo
      icon={icon}
      name={name}
      value={value}
      inline={inline}
    />
  );
}

export default EntityMetaInfo;
