import * as React from 'react';

import ActivityLogs from '../../containers/activityLogs';
import Breadcrumb from '../breadcrumb';

function HistoryLogs() {
  return (
    <div className="row">
      <div className="col-md-12">
        <Breadcrumb
          icon="fas fa-history"
          links={[
            {name: 'Recently viewed'}]}
        />
        <ActivityLogs history={true}/>
      </div>
    </div>
  );
}

export default HistoryLogs;
