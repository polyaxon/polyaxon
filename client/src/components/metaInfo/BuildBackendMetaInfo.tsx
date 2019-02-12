import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  value: string | number;
  inline?: boolean;
}

function BuildBackendMetaInfo({value, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fa-bars"
      name="Backend"
      value={value || 'native'}
      inline={inline}
    />
  );
}

export default BuildBackendMetaInfo;
