import * as React from 'react';
import * as _ from 'lodash';

import { ExperimentModel } from '../models/experiment';
import Status from './status';
import Description from './description';
import UserMetaInfo from './metaInfo/userMetaInfo';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import MetaInfo from './metaInfo/metaInfo';
import GridList from './gridList';
import { EmptyList } from './emptyList';
import { getExperimentTensorboardUrl } from '../constants/utils';
import Tags from './tags';

export interface Props {
  experiment: ExperimentModel;
}

export default class ExperimentOverview extends React.Component<Props, Object> {
  public render() {
    const experiment = this.props.experiment;

    if (_.isNil(experiment)) {
      return EmptyList(false, 'experiment', 'experiment');
    }
    return (
      <div className="entity-details">
        <div className="row">
          <div className="col-md-12">
            <Description
              description={experiment.description}
              showEmpty={true}
            />
            <div className="meta">
              <UserMetaInfo user={experiment.user} inline={true}/>
              <DatesMetaInfo
                createdAt={experiment.created_at}
                updatedAt={experiment.updated_at}
                inline={true}
              />
              <MetaInfo
                icon="fa-cube"
                name="Jobs"
                value={experiment.num_jobs}
                inline={true}
              />
            </div>
            <div className="meta">
              <TaskRunMetaInfo startedAt={experiment.started_at} finishedAt={experiment.finished_at} inline={true}/>
              <Status status={experiment.last_status}/>
            </div>
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
            {experiment.has_tensorboard &&
            <div className="meta">
              <span className="meta-info meta-dashboard">
                <i className="fa fa-link icon" aria-hidden="true"/>
                <a
                  href={getExperimentTensorboardUrl(experiment.project, experiment.id)}
                  className="title-link"
                >Tensorboard
                </a>
              </span>
            </div>
            }
            <Tags tags={experiment.tags}/>
            {experiment.declarations &&
            <div className="meta meta-declarations">
              <span className="meta-info">
                <i className="fa fa-gear icon" aria-hidden="true"/>
                <span className="title">Declarations:</span>
              </span>
              <GridList rows={[experiment.declarations]}/>
            </div>
            }
            {experiment.last_metric &&
            <div className="meta meta-metrics">
              <span className="meta-info">
                <i className="fa fa-area-chart icon" aria-hidden="true"/>
                <span className="title">Metrics:</span>
              </span>
              <GridList rows={[experiment.last_metric]}/>
            </div>
            }
          </div>
        </div>
      </div>
    );
  }
}
