import * as moment from 'moment';
import * as React from 'react';

import MetaInfo from './metaInfo';

export interface Props {
  datetime: Date | string;
  inline?: boolean;
}

function DateMetaInfo({datetime, inline = false}: Props) {
  const datetimeM = moment(datetime);
  return (
    <MetaInfo
      icon="far fa-clock"
      name="Created"
      tooltip={datetimeM.format('YYYY-MM-DD HH:mm:ss')}
      value={datetimeM.fromNow()}
      inline={inline}
    />
  );
}

export default DateMetaInfo;
