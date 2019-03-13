import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  value: string | number;
  inline?: boolean;
}

function BackendMetaInfo({value, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fas fa-bars"
      name="Backend"
      value={value || 'native'}
      inline={inline}
    />
  );
}

export default BackendMetaInfo;
