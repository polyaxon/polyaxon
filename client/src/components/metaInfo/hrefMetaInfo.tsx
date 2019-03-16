import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  icon: string;
  name: string;
  value: string;
  link?: string;
  inline?: boolean;
}

function HrefMetaInfo({icon, name, value, link, inline = false}: Props) {
  if (link) {
    return (
      <MetaInfo
        icon={icon}
        name={name}
        value={<a href={link}>{value}</a>}
        inline={inline}
      />
    );
  }
  return (null);
}

export default HrefMetaInfo;
