import * as React from 'react';

import './instructions.less';

export interface Props {
  id: number | string;
}

function TensorboardInstructions({id}: Props) {
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
              <h4>Give the tensorboard a unique name</h4>
              <div className="instructions-section-content">
                polyaxon tensorboard -b {id} update --name=tensorboard_unique
              </div>
            </div>
            <div className="instructions-section">
              <h4>Add/update the tensorboard's description</h4>
              <div className="instructions-section-content">
                polyaxon tensorboard -b {id} update --description="New tensorboard description..."
              </div>
            </div>
            <div className="instructions-section">
              <h4>Add/update the tensorboard's tags</h4>
              <div className="instructions-section-content">
                polyaxon tensorboard -b {id} update --tags="foo, bar, ..,"
              </div>
            </div>
            <div className="instructions-section">
              <h4>Bookmark tensorboard</h4>
              <div className="instructions-section-content">
                polyaxon tensorboard -b {id} bookmark
              </div>
              <div className="instructions-section-content">
                polyaxon tensorboard -b {id} unbookmark
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default TensorboardInstructions;
