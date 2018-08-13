import * as React from 'react';

import LinkMetaInfo from './linkMetaInfo';

export interface Props {
  value: string;
  link: string;
  inline?: boolean;
}

function BuildLinkMetaInfo({value, link, inline = false}: Props) {
  return (
    <LinkMetaInfo
      icon="fa-gavel"
      name="Build"
      value={value}
      link={link}
      inline={inline}
    />
  );
}

export default BuildLinkMetaInfo;
