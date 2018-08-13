import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  commit: string;
  inline?: boolean;
}

function CommitMetaInfo({commit, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fa-hashtag"
      name="Commit"
      value={commit}
      inline={inline}
    />
  );
}

export default CommitMetaInfo;
