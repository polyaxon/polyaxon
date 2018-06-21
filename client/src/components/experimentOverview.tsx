import * as React from 'react';
import * as _ from 'lodash';
import * as moment from 'moment';

import { ExperimentModel } from '../models/experiment';
import ExperimentJobs from '../containers/experimentJobs';
import Logs from '../containers/logs';
import TaskRunMetaInfo from './taskRunMetaInfo';
import Status from './status';
import Description from './description';

export interface Props {
  experiment: ExperimentModel;
}

export default class ExperimentOverview extends React.Component<Props, Object> {
  public render() {
    const experiment = this.props.experiment;

    if (_.isNil(experiment)) {
      return (<div>Nothing</div>);
    }
    return (
      <div className="entity-details">
        <div className="row">
          <div className="col-md-12">
             <Description
                description={experiment.description}
                entity="experiment"
                command="polyaxon experiment update --description=..."
             />
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
              <Status status={experiment.last_status}/>
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
        </div>
      </div>
    );
  }
}
