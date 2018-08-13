import * as React from 'react';

import MetaInfo from '../metaInfo';

export interface Props {
  count: number;
  inline?: boolean;
}

function ExperimentCountMetaInfo({count, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fa-cube"
      name="Experiments"
      value={count}
      inline={inline}
    />
  );
}

export default ExperimentCountMetaInfo;
