import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  concurrency: number;
  inline?: boolean;
}

function ConcurrencyMetaInfo({concurrency, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fa-gears"
      name="Concurrency"
      value={concurrency}
      inline={inline}
    />
  );
}

export default ConcurrencyMetaInfo;
