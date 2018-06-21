import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  user: string;
  inline?: boolean;
}

function UserMetaInfo({user, inline = false}: Props) {
  return (
    <MetaInfo
      icon="fa-user-o"
      name="User"
      value={user}
      inline={inline}
    />
  );
}

export default UserMetaInfo;
