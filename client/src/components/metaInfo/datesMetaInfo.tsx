import * as React from 'react';
import * as moment from 'moment';

import MetaInfo from './metaInfo';

export interface Props {
  createdAt?: Date | string;
  updatedAt?: Date | string;
  inline?: boolean;
}

function DatesMetaInfo({createdAt, updatedAt, inline = false}: Props) {
  return (
    <span>
        {createdAt &&
        <MetaInfo
          icon="fa-clock-o"
          name="Created"
          value={moment(createdAt).fromNow()}
          inline={inline}
        />
        }
      {updatedAt &&
      <MetaInfo
        icon="fa-clock-o"
        name="Last updated"
        value={moment(updatedAt).fromNow()}
        inline={inline}
      />
      }
    </span>
  );
}

export default DatesMetaInfo;
