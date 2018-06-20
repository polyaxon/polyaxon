import * as React from 'react';

function ExperimentHeader() {
  return (
    <div className="row">
      <div className="col-md-1 block">
        Status
      </div>
      <div className="col-md-7 block">
        Name
      </div>
      <div className="col-md-2 block">
        Metrics
      </div>
      <div className="col-md-2 block">
        Info
      </div>
    </div>
  );
}

export default ExperimentHeader;
