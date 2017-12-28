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
  
  let buildJobsUrl = function (experiment: ExperimentModel) {
    let projectNameAndUser = urlifyProjectName(experiment.project_name)
    return `/${projectNameAndUser}/experiments/${experiment.sequence}`
  }
  
  return (
    <div className="row">
      <div className="col-md-12 experiment">
        <ButtonToolbar className="pull-right">
          <LinkContainer to={ buildJobsUrl(experiment) }><Button>View experiment details</Button></LinkContainer>
        </ButtonToolbar>
        <h4 className="title"><a>{ experiment.unique_name}</a></h4>
      </div>
    </div>
  );
}

export default Experiment;
