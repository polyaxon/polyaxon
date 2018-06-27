import * as React from 'react';
import './instructions.less';

export interface Props {
  id: number | string;
}

function GroupInstructions({id}: Props) {
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
                polyaxon group -g {id} update --description="New group description..."
              </div>
            </div>
            <div className="instructions-section">
              <h4>Add/update the project tags</h4>
              <div className="instructions-section-content">
                polyaxon group -g {id} update --tags="foo, bar, ..,"
              </div>
            </div>
            <div className="instructions-section">
              <h4>Start a tensorboard</h4>
              <div className="instructions-section-content">
                polyaxon tensorboard start -g {id} [-f polyaxonfile.yml] [-f override_file.yml] [-u]
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default GroupInstructions;
