import * as React from 'react';

import { CloningInterface } from '../../interfaces/cloning';
import LinkMetaInfo from './linkMetaInfo';

export interface Props {
  cloning: CloningInterface;
  inline?: boolean;
}

function CloningLinkMetaInfo({cloning, inline = false}: Props) {
  return (
    <LinkMetaInfo
      icon="fa-clone"
      name={cloning.strategy}
      value={cloning.original}
      link={cloning.link}
      inline={inline}
    />
  );
}

export default CloningLinkMetaInfo;
