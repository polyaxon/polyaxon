import * as React from 'react';

import { StatusModel } from '../models/status';
import Status from './status';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import Description from './description';

export interface Props {
  status: StatusModel;
}

function StatusItem({status}: Props) {
  return (
    <div className="row">
      <div className="col-md-2 block">
        <Status status={status.status}/>
      </div>
      <div className="col-md-3 block">
        <div className="meta">
          <DatesMetaInfo
            createdAt={status.created_at}
            inline={true}
          />
        </div>
      </div>
      <div className="col-md-7 block">
        <Description description={status.message}/>
      </div>
    </div>
  );
}

export default StatusItem;
