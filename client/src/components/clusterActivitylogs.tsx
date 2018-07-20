import * as React from 'react';

import Breadcrumb from './breadcrumb';
import ActivityLogs from '../containers/activityLogs';

function ClusterActivityLogs() {
  return (
    <div className="row">
      <div className="col-md-12">
        <Breadcrumb
          icon="fa-align-justify"
          links={[
            {name: 'activities'}]}
        />
       <ActivityLogs />
      </div>
    </div>
  );
}

export default ClusterActivityLogs;
