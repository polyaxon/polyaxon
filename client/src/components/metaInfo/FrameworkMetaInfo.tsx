import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  value: string | number;
  inline?: boolean;
}

function FrameworkMetaInfo({value, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fas fa-project-diagram"
      name="Framework"
      value={value}
      inline={inline}
    />
  );
}

export default FrameworkMetaInfo;
