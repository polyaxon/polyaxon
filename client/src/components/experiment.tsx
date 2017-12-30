import * as React from "react";

import {Button, ButtonToolbar} from "react-bootstrap";
import {LinkContainer} from "react-router-bootstrap";
import {dateOptions, urlifyProjectName} from "../constants/utils"

import {ExperimentModel} from "../models/experiment";


export interface Props {
  experiment: ExperimentModel;
  onDelete: () => void;
}


function Experiment({experiment, onDelete}: Props) {
  
  return (
    <div className="row">
      <div className="col-md-12 block">
        <ButtonToolbar className="pull-right">
          <LinkContainer to={ `${experiment.sequence}/` }>
            <Button className="button">
              { experiment.num_jobs } Job{ experiment.num_jobs != 1 && 's' }
              <i className="fa fa-cube icon" aria-hidden="true"></i>
            </Button>
          </LinkContainer>
        </ButtonToolbar>
        <span className="title">
          <i className="fa fa-sliders icon" aria-hidden="true"></i>
          { experiment.unique_name}
          <span className="status">({ experiment.last_status})</span>
        </span>
        <div className="meta">
          <i className="fa fa-user-o icon" aria-hidden="true"></i>
          <span className="title">User:</span>
          { experiment.user }
        </div>
        { experiment.started_at &&
        <div className="meta">
          <i className="fa fa-clock-o icon" aria-hidden="true"></i>
          <span className="title">Started at:</span>
          { experiment.started_at }
        </div>
        }
        { experiment.finished_at &&
        <div className="meta">
          <i className="fa fa-clock-o icon" aria-hidden="true"></i>
          <span className="title">Finished at:</span>
          { experiment.finished_at }
        </div>
        }
      </div>
    </div>
  );
}

export default Experiment;
