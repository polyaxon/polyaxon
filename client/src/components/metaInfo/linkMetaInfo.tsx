import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import MetaInfo from './metaInfo';

export interface Props {
  icon: string;
  name: string;
  value: string;
  link?: string;
  inline?: boolean;
}

function LinkMetaInfo({icon, name, value, link, inline = false}: Props) {
  if (link) {
    return (
      <MetaInfo
        icon={icon}
        name={name}
        value={<LinkContainer to={link}><a>{value}</a></LinkContainer>}
        inline={inline}
      />
    );
  }
  return (null);
}

export default LinkMetaInfo;
