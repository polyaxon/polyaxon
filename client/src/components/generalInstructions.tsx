import * as React from 'react';
import './instructions.less';

export interface Props {
  entity: string;
  entityId: number | string;
}

function GeneralInstructions({entity, entityId}: Props) {
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
              <h4>Add/update the build description</h4>
              <div className="instructions-section-content">
                polyaxon entity -b {entityId} update --description="New {entity} description..."
              </div>
            </div>
            <div className="instructions-section">
              <h4>Add/update the project tags</h4>
              <div className="instructions-section-content">
                polyaxon entity -b {entityId} update --tags="foo, bar, ..,"
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default GeneralInstructions;
