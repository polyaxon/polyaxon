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
              <h4>Filters</h4>
              <ul>
                <li>
                  <a href="https://docs.polyaxon.com/query_syntax/introduction//">
                    Understanding the query syntax
                  </a>
                </li>
                <li>
                  <a href="https://docs.polyaxon.com/query_syntax/entities/experiments/">
                    Searching Experiments
                  </a>
                </li>
              </ul>
            </div>
            <div className="instructions-section">
              <h4>Give the group a unique name</h4>
              <div className="instructions-section-content">
                polyaxon group -g -xp {id} update --name=experiment_to_test_x
              </div>
            </div>
            <div className="instructions-section">
              <h4>Add/update the group's description</h4>
              <div className="instructions-section-content">
                polyaxon group -g {id} update --description="New group description..."
              </div>
            </div>
            <div className="instructions-section">
              <h4>Add/update the group's tags</h4>
              <div className="instructions-section-content">
                polyaxon group -g {id} update --tags="foo, bar, ..,"
              </div>
            </div>
            <div className="instructions-section">
              <h4>Start a tensorboard for the group</h4>
              <div className="instructions-section-content">
                polyaxon tensorboard -g {id} start [-f polyaxonfile.yml] [-f override_file.yml] [-u]
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default GroupInstructions;
