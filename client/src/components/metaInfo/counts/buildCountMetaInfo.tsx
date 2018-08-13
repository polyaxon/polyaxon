import * as React from 'react';

import MetaInfo from '../metaInfo';

export interface Props {
  count: number;
  inline?: boolean;
}

function BuildCountMetaInfo({count, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fa-gavel"
      name="Builds"
      value={count}
      inline={inline}
    />
  );
}

export default BuildCountMetaInfo;
