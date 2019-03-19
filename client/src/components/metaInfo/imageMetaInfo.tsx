import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  value: string;
  link: string;
  inline?: boolean;
}

function ImageMetaInfo({value, link, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fas fa-gavel"
      name="Image"
      value={value}
      inline={inline}
    />
  );
}

export default ImageMetaInfo;
