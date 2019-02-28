import * as React from 'react';

import './instructions.less';

export interface Props {
  id: number | string;
}

function ExperimentJobInstructions({id}: Props) {
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
              <h4>List jobs under an experiment</h4>
              <div className="instructions-section-content">
                polyaxon experiment -xp {id} jobs
              </div>
            </div>
            <div className="instructions-section">
              <h4>Logs of an experiment job</h4>
              <div className="instructions-section-content">
                polyaxon experiment -xp {id} logs -j {id} --past --follow
              </div>
            </div>
            <div className="instructions-section">
              <h4>List statuses of an experiment job</h4>
              <div className="instructions-section-content">
                polyaxon experiment -xp {id} statuses -j {id}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ExperimentJobInstructions;
