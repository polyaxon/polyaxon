import * as React from 'react';

import MetaInfo from '../metaInfo';

export interface Props {
  count: number;
  inline?: boolean;
}

function GroupCountMetaInfo({count, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fa-cubes"
      name="Experiment Groups"
      value={count}
      inline={inline}
    />
  );
}

export default GroupCountMetaInfo;
