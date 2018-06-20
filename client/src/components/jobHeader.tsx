import * as React from 'react';

function JobHeader() {
  return (
    <div className="row">
      <div className="col-md-1 block">
        Status
      </div>
      <div className="col-md-9 block">
        Name
      </div>
      <div className="col-md-2 block">
        Info
      </div>
    </div>
  );
}

export default JobHeader;
