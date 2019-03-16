import * as React from 'react';

import './instructions.less';

export interface Props {
  id: number | string;
}

function NotebookInstructions({id}: Props) {
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
              <h4>Give the notebook a unique name</h4>
              <div className="instructions-section-content">
                polyaxon notebook -b {id} update --name=notebook_unique
              </div>
            </div>
            <div className="instructions-section">
              <h4>Add/update the notebook's description</h4>
              <div className="instructions-section-content">
                polyaxon notebook -b {id} update --description="New notebook description..."
              </div>
            </div>
            <div className="instructions-section">
              <h4>Add/update the notebook's tags</h4>
              <div className="instructions-section-content">
                polyaxon notebook -b {id} update --tags="foo, bar, ..,"
              </div>
            </div>
            <div className="instructions-section">
              <h4>Bookmark notebook</h4>
              <div className="instructions-section-content">
                polyaxon notebook -b {id} bookmark
              </div>
              <div className="instructions-section-content">
                polyaxon notebook -b {id} unbookmark
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default NotebookInstructions;
