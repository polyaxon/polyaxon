import * as React from "react";
import * as moment from "moment";
import {LinkContainer} from "react-router-bootstrap";

import {
  getCssClassForStatus,
  getExperimentUrl,
  humanizeTimeDelta,
  splitProjectName
} from "../constants/utils"

import {ExperimentModel} from "../models/experiment";


export interface Props {
  experiment: ExperimentModel;
  onDelete: () => void;
}


function Experiment({experiment, onDelete}: Props) {
  let totalRun = humanizeTimeDelta(experiment.started_at, experiment.finished_at);
  let statusCssClass = getCssClassForStatus(experiment.last_status);
  let values = splitProjectName(experiment.project_name);
  return (
    <div className="row">
      <div className="col-md-10 block">
        <LinkContainer to={getExperimentUrl(values[0], values[1], experiment.sequence)}>
          <a className="title">
            <i className="fa fa-cube icon" aria-hidden="true"></i>
            {experiment.unique_name}
            <span className={`status alert alert-${statusCssClass}`}>{experiment.last_status}</span>
          </a>
        </LinkContainer>
        <div className="meta-description">
          {experiment.description}
        </div>
        <div className="meta">
          <span className="meta-info">
            <i className="fa fa-user-o icon" aria-hidden="true"></i>
            <span className="title">User:</span>
            {experiment.user}
          </span>
          <span className="meta-info">
              <i className="fa fa-clock-o icon" aria-hidden="true"></i>
            <span className="title">Created:</span>
            {moment(experiment.created_at).fromNow()}
          </span>
        </div>
      </div>

      <div className="col-md-2 block">
        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-tasks icon" aria-hidden="true"></i>
            <span className="title">Jobs:</span>
            {experiment.num_jobs}
          </span>
        </div>
        {experiment.started_at &&
        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-clock-o icon" aria-hidden="true"></i>
            <span className="title">Started:</span>
            {moment(experiment.started_at).fromNow()}
          </span>
        </div>
        }
        {experiment.finished_at &&
        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-clock-o icon" aria-hidden="true"></i>
            <span className="title">Finished:</span>
            {moment(experiment.finished_at).fromNow()}
          </span>
        </div>
        }
        {totalRun &&
        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-hourglass icon" aria-hidden="true"></i>
            <span className="title">Total run:</span>
            {totalRun}
          </span>
        </div>
        }
      </div>
    </div>
  );
}

export default Experiment;
