import * as React from 'react';

import LinkMetaInfo from './linkMetaInfo';

export interface Props {
  value: string;
  link: string;
  inline?: boolean;
}

function GroupLinkMetaInfo({value, link, inline = false}: Props) {
  return (
    <LinkMetaInfo
      icon="fa-cubes"
      name="Group"
      value={value}
      link={link}
      inline={inline}
    />
  );
}

export default GroupLinkMetaInfo;
