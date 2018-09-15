import * as React from 'react';

import ActivityLogs from '../../containers/activityLogs';
import Breadcrumb from '../breadcrumb';

function ClusterActivityLogs() {
  return (
    <div className="row">
      <div className="col-md-12">
        <Breadcrumb
          icon="fa-align-justify"
          links={[
            {name: 'activities'}]}
        />
        <ActivityLogs/>
      </div>
    </div>
  );
}

export default ClusterActivityLogs;
