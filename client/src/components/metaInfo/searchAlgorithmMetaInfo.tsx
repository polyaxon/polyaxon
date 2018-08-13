import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  searchAlgorithm: string;
  inline?: boolean;
}

function SearchAlgorithmMetaInfo({searchAlgorithm, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fa-asterisk"
      name="Algorithm"
      value={searchAlgorithm}
      inline={inline}
    />
  );
}

export default SearchAlgorithmMetaInfo;
