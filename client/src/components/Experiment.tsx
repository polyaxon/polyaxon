import * as React from "react";
import {Button, ButtonToolbar} from "react-bootstrap";

import {ExperimentModel} from "../models/experiment";


export interface Props {
  experiment: ExperimentModel;
  onDelete?: () => void;
}


function Experiment({experiment, onDelete}: Props) {
  return (
    <div className="row">
      <div className="col-md-12 experiment">
        <h4 className="title"><a>{ experiment.name }</a></h4>
        <div className="meta">{ experiment.createdAt.toLocaleTimeString() }</div>
        <ButtonToolbar className="pull-right">
          <Button>View</Button>
          <Button bsStyle="danger" className="pull-right" onClick={onDelete}>delete</Button>
        </ButtonToolbar>
      </div>
    </div>
  );
}

export default Experiment;
