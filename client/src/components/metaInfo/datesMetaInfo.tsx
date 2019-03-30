import * as moment from 'moment';
import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  createdAt?: Date | string;
  updatedAt?: Date | string;
  inline?: boolean;
}

function DatesMetaInfo({createdAt, updatedAt, inline = false}: Props) {
  const createdAtM = createdAt ? moment(createdAt) : null;
  const updatedAtM = updatedAt ? moment(updatedAt) : null;
  return (
    <span>
        {createdAtM &&
        <MetaInfo
          icon="far fa-clock"
          name="Created"
          tooltip={createdAtM.format('YYYY-MM-DD HH:mm:ss')}
          value={createdAtM.fromNow()}
          inline={inline}
        />
        }
      {updatedAtM &&
      <MetaInfo
        icon="far fa-clock"
        name="Last updated"
        tooltip={updatedAtM.format('YYYY-MM-DD HH:mm:ss')}
        value={updatedAtM.fromNow()}
        inline={inline}
      />
      }
    </span>
  );
}

export default DatesMetaInfo;
