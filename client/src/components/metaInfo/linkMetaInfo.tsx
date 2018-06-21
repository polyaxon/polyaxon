import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import MetaInfo from './metaInfo';

export interface Props {
  icon: string;
  name: string;
  value: string;
  inline?: boolean;
}

function LinkMetaInfo({icon, name, value, inline = false}: Props) {
  return (<MetaInfo icon={icon} name={name} value={<LinkContainer to={value} />} inline={inline}/>);
}

export default LinkMetaInfo;
