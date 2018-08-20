import * as React from 'react';

function BuildHeader() {
  return (
    <div className="row">
      <div className="col-md-1 block">
        Status
      </div>
      <div className="col-md-8 block">
        Name
      </div>
      <div className="col-md-2 block">
        Run
      </div>
      <div className="col-md-1 block">
        Actions
      </div>
    </div>
  );
}

export default BuildHeader;
