import * as React from "react";
import {Button, ButtonToolbar} from "react-bootstrap";
import {LinkContainer} from "react-router-bootstrap";
import {dateOptions} from "../constants/utils"

import {ExperimentModel} from "../models/experiment";


export interface Props {
  experiment: ExperimentModel;
  onDelete: () => void;
}


function Experiment({experiment, onDelete}: Props) {
  
  let buildJobsUrl = function (experiment: ExperimentModel) {
    let projectName = experiment.project_name.substr(experiment.project_name.indexOf('.') + 1)
    return `/admin/${projectName}/experiments/${experiment.sequence}/jobs`
  }
  
  return (
    <div className="row">
      <div className="col-md-12 experiment">
        <ButtonToolbar className="pull-right">
          <LinkContainer to={ buildJobsUrl(experiment) }><Button>View jobs</Button></LinkContainer>
        </ButtonToolbar>
        <h4 className="title"><a>{ experiment.unique_name}</a></h4>
        <div className="meta"><b>Uuid: </b>{ experiment.uuid}</div>
        <div className="meta"><b>Sequence: </b>{ experiment.sequence}</div>
        <div className="meta"><b>Description: </b>{ experiment.uuid}</div>
        {experiment.experiment_group_name && <div className="meta"><b>Group: </b>{ experiment.experiment_group_name }</div>}
        <div className="meta"><b>User: </b>{ experiment.user }</div>
        <div className="meta"><b>Content: </b>{ experiment.content }</div>
        <div className="meta"><b>Created at: </b>{ experiment.createdAt.toLocaleTimeString("en-US", dateOptions) }</div>
        <div className="meta"><b>Updated at: </b>{ experiment.updatedAt.toLocaleTimeString("en-US", dateOptions) }</div>
      </div>
    </div>
  );
}

export default Experiment;
