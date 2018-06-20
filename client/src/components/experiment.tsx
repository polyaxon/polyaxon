import * as React from 'react';
import * as moment from 'moment';
import { LinkContainer } from 'react-router-bootstrap';

import {
  getExperimentUrl,
  splitProjectName
} from '../constants/utils';

import { ExperimentModel } from '../models/experiment';
import TaskRunMetaInfo from './taskRunMetaInfo';
import Status from './status';

export interface Props {
  experiment: ExperimentModel;
  onDelete: () => void;
}

function Experiment({experiment, onDelete}: Props) {
  let values = splitProjectName(experiment.project_name);
  return (
    <div className="row">
      <div className="col-md-1 block">
        <Status status={experiment.last_status}/>
      </div>
      <div className="col-md-7 block">
        <LinkContainer to={getExperimentUrl(values[0], values[1], experiment.id)}>
          <a className="title">
            <i className="fa fa-cube icon" aria-hidden="true"/>
            {experiment.unique_name}
          </a>
        </LinkContainer>
        <div className="meta-description">
          {experiment.description}
        </div>
        <div className="meta">
          <span className="meta-info">
            <i className="fa fa-user-o icon" aria-hidden="true"/>
            <span className="title">User:</span>
            {experiment.user}
          </span>
          <span className="meta-info">
              <i className="fa fa-clock-o icon" aria-hidden="true"/>
            <span className="title">Created:</span>
            {moment(experiment.created_at).fromNow()}
          </span>
        </div>
      </div>
      <div className="col-md-2 block">
        {experiment.last_metric &&
        <div className="meta-metrics">
          {Object.keys(experiment.last_metric).map(
            (xp, idx) =>
              <div className="row meta" key={idx}>
                <span className="meta-info">
                  <i className="fa fa-area-chart icon" aria-hidden="true"/>
                  <span className="title">{xp}:</span>
                  {experiment.last_metric[xp]}
                </span>
              </div>)}
        </div>
        }
      </div>
      <div className="col-md-2 block">
        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-tasks icon" aria-hidden="true"/>
            <span className="title">Jobs:</span>
            {experiment.num_jobs}
          </span>
        </div>
        <TaskRunMetaInfo startedAt={experiment.started_at} finishedAt={experiment.finished_at}/>
      </div>
    </div>
  );
}

export default Experiment;
