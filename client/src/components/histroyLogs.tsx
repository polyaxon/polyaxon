import * as React from 'react';

import Breadcrumb from './breadcrumb';
import ActivityLogs from '../containers/activityLogs';

function HistoryLogs() {
  return (
    <div className="row">
      <div className="col-md-12">
        <Breadcrumb
          icon="fa-history"
          links={[
            {name: 'History'}]}
        />
       <ActivityLogs history={true} />
      </div>
    </div>
  );
}

export default HistoryLogs;
