import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  value: string | number;
  inline?: boolean;
}

function IdMetaInfo({value, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fa-circle"
      name="id"
      value={value}
      inline={inline}
    />
  );
}

export default IdMetaInfo;
