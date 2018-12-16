import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  value: string | number;
  inline?: boolean;
}

function PodIdMetaInfo({value, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fa-circle-o"
      name="Pod"
      value={value}
      inline={inline}
    />
  );
}

export default PodIdMetaInfo;
