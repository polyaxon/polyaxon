import * as React from 'react';

import { StatusModel } from '../models/status';
import Description from './description';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import Status from './status';

export interface Props {
  status: StatusModel;
  onClick: () => void;
}

function StatusItem({status, onClick}: Props) {
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
        {status.traceback &&
        <button className="btn btn-xs btn-default pull-left btn-traceback" onClick={onClick}>
          <i className="fa fa-question icon" aria-hidden="true"/>
        </button>
        }<Description description={status.message}/>
      </div>
    </div>
  );
}

export default StatusItem;
