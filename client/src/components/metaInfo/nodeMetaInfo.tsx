import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  node: string;
  inline?: boolean;
}

function NodeMetaInfo({node, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fas fa-th"
      name="Node"
      tooltip="Node where this job was scheduled"
      value={node}
      inline={inline}
    />
  );
}

export default NodeMetaInfo;
