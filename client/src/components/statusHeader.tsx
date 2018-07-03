import * as React from 'react';

function StatusHeader() {
  return (
    <div className="row">
      <div className="col-md-2 block">
        Status
      </div>
      <div className="col-md-3 block">
        Created at
      </div>
      <div className="col-md-7 block">
        Details
      </div>
    </div>
  );
}

export default StatusHeader;
