import * as React from 'react';
import './instructions.less';

export interface Props {
  id: number | string;
}

function BuildInstructions({id}: Props) {
  return (
    <div className="instructions">
      <div className="row">
        <div className="col-md-12">
          <div className="instructions-header">
            Instructions
          </div>
        </div>
      </div>
      <div className="row">
        <div className="col-md-12">
          <div className="instructions-content">
            <div className="instructions-section">
              <h4>Give the build a unique name</h4>
              <div className="instructions-section-content">
                polyaxon build -b {id} update --name=build_unique
              </div>
            </div>
            <div className="instructions-section">
              <h4>Add/update the build's description</h4>
              <div className="instructions-section-content">
                polyaxon build -b {id} update --description="New build description..."
              </div>
            </div>
            <div className="instructions-section">
              <h4>Add/update the build's tags</h4>
              <div className="instructions-section-content">
                polyaxon build -b {id} update --tags="foo, bar, ..,"
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default BuildInstructions;
