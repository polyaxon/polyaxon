import * as React from 'react';

import { ActivityLogModel } from '../models/activitylog';

export interface Props {
  activityLog: ActivityLogModel;
}

function ActivityLog({activityLog}: Props) {
  return (
    <div className="row">
      <div className="col-md-2 block">
        <span>{activityLog.created_at}</span>
      </div>
      <div className="col-md-9 block">
        <span>{activityLog.event_type}</span>
      </div>
    </div>
  );
}

export default ActivityLog;
