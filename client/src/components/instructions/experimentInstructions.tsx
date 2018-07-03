import * as React from 'react';
import './instructions.less';

export interface Props {
  id: number | string;
}

function ExperimentInstructions({id}: Props) {
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
              <h4>Give the experiment a unique name</h4>
              <div className="instructions-section-content">
                polyaxon experiment -xp {id} update --name=experiment_to_test_x
              </div>
            </div>
            <div className="instructions-section">
              <h4>Add/update the experiment description</h4>
              <div className="instructions-section-content">
                polyaxon experiment -xp {id} update --description="New experiment description..."
              </div>
            </div>
            <div className="instructions-section">
              <h4>Add/update the experiment tags</h4>
              <div className="instructions-section-content">
                polyaxon experiment -xp {id} update --tags="foo, bar, ..,"
              </div>
            </div>
            <div className="instructions-section">
              <h4>Start a tensorboard for experiment</h4>
              <div className="instructions-section-content">
                polyaxon tensorboard start -xp {id} [-f polyaxonfile.yml] [-f override_file.yml] [-u]
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ExperimentInstructions;
