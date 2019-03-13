import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  groupTyp: string;
  inline?: boolean;
}

function GroupType({groupTyp, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fas fa-layer-group"
      name="Type"
      value={groupTyp}
      inline={inline}
    />
  );
}

export default GroupType;
