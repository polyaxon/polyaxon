import * as React from "react";
import {Button} from "react-bootstrap";

import {ExperimentModel} from "../models/experiment";


export interface Props {
  experiment: ExperimentModel;
  onDelete?: () => void;
}


function Experiment({experiment, onDelete}: Props) {
  return (
    <div className="experiment">
      {experiment.name}
      <Button className="warning" onClick={onDelete}>delete</Button>
    </div>
  );
}

export default Experiment;
