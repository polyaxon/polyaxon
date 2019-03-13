import * as React from 'react';

import MetaInfo from '../metaInfo';

export interface Props {
  count: number;
  inline?: boolean;
}

function JobCountMetaInfo({count, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fas fa-tasks"
      name="Jobs"
      value={count}
      inline={inline}
    />
  );
}

export default JobCountMetaInfo;
