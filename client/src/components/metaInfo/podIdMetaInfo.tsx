import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  value: string | number;
  inline?: boolean;
}

function PodIdMetaInfo({value, inline = false}: Props) {
  return (
    <MetaInfo
      icon="far fa-circle"
      name="Pod"
      value={value}
      inline={inline}
    />
  );
}

export default PodIdMetaInfo;
