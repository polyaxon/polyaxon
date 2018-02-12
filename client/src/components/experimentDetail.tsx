import * as React from 'react';
import * as _ from 'lodash';
import * as moment from 'moment';
import { LinkContainer } from 'react-router-bootstrap';

import { ExperimentModel } from '../models/experiment';
import Jobs from '../containers/jobs';
import {
  getGroupUrl,
  getProjectUrl,
  getUserUrl,
  splitGroupName,
  splitProjectName,
  getCssClassForStatus,
} from '../constants/utils';
import TaskRunMetaInfo from './taskRunMetaInfo';

export interface Props {
  experiment: ExperimentModel;
  onDelete: () => any;
  fetchData: () => any;
}

export default class ExperimentDetail extends React.Component<Props, Object> {
  componentDidMount() {
    const {experiment, onDelete, fetchData} = this.props;
    fetchData();
  }

  public render() {
    const {experiment, onDelete, fetchData} = this.props;

    if (_.isNil(experiment)) {
      return (<div>Nothing</div>);
    }
    let statusCssClass = getCssClassForStatus(experiment.last_status);
    let values = splitProjectName(experiment.project_name);
    let group = null;
    if (!_.isNil(experiment.experiment_group_name)) {
      group = parseInt(splitGroupName(experiment.experiment_group_name)[2], 10);
    }
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <span className="title">
              <i className="fa fa-cube icon" aria-hidden="true"/>
              <LinkContainer to={getUserUrl(values[0])}>
                <span>
                  <a className="title">
                    {values[0]}
                  </a>/
                </span>
              </LinkContainer>
              <LinkContainer to={getProjectUrl(values[0], values[1])}>
                <span>
                  <a className="title">
                    {values[1]}
                  </a>/
                </span>
              </LinkContainer>
              {group &&
              <LinkContainer to={getGroupUrl(values[0], values[1], group)}>
                <span>
                  <a className="title">
                    Group {group}
                  </a>/
                </span>
              </LinkContainer>
              }
              <span className="title">
                Experiment {experiment.sequence}
              </span>
            </span>
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
              <span className="meta-info">
                <i className="fa fa-tasks icon" aria-hidden="true"/>
                <span className="title">Jobs:</span>
                {experiment.num_jobs}
              </span>
              <TaskRunMetaInfo startedAt={experiment.started_at} finishedAt={experiment.finished_at} inline={true}/>
              <span className={`status alert alert-${statusCssClass}`}>{experiment.last_status}
              </span>
            </div>
            {experiment.last_metric &&
            <div className="meta meta-metrics">
              {Object.keys(experiment.last_metric).map(
                (xp, idx) =>
                  <span className="meta-info" key={idx}>
                  <i className="fa fa-area-chart icon" aria-hidden="true"/>
                  <span className="title">{xp}:</span>
                    {experiment.last_metric[xp]}
                </span>)}
            </div>
            }
            {experiment.resources &&
            <div className="meta meta-resources">
              {Object.keys(experiment.resources)
                .filter(
                  (res, idx) =>
                    experiment.resources[res] != null
                )
                .map(
                  (res, idx) =>
                    <span className="meta-info" key={idx}>
                <i className="fa fa-microchip icon" aria-hidden="true"/>
                <span className="title">{res}:</span>
                      {experiment.resources[res].requests || ''} - {experiment.resources[res].limits || ''}
              </span>
                )}
            </div>
            }
            {experiment.declarations &&
            <div className="meta meta-declarations">
              {Object.keys(experiment.declarations).map(
                (xp, idx) =>
                  <span className="meta-info" key={idx}>
                  <i className="fa fa-gear icon" aria-hidden="true"/>
                  <span className="title">{xp}:</span>
                    {experiment.declarations[xp]}
                </span>)}
            </div>
            }
          </div>
          <h4 className="polyaxon-header">Jobs</h4>
          <Jobs fetchData={() => null} user={experiment.user} experiment={experiment}/>
        </div>
      </div>
    );
  }
}
