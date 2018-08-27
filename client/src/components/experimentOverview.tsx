import * as _ from 'lodash';
import * as React from 'react';

import { getExperimentTensorboardUrl } from '../constants/utils';
import { ExperimentModel } from '../models/experiment';
import Description from './description';
import { EmptyList } from './empty/emptyList';
import GridTable from './gridTable';
import JobCountMetaInfo from './metaInfo/counts/jobCountMetaInfo';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import ResourcesMetaInfo from './metaInfo/resourcesMetaInfo';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import UserMetaInfo from './metaInfo/userMetaInfo';
import Status from './status';
import Tags from './tags';

export interface Props {
  experiment: ExperimentModel;
}

export default class ExperimentOverview extends React.Component<Props, {}> {
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
              <JobCountMetaInfo count={experiment.num_jobs} inline={true}/>
            </div>
            <div className="meta">
              <TaskRunMetaInfo startedAt={experiment.started_at} finishedAt={experiment.finished_at} inline={true}/>
              <Status status={experiment.last_status}/>
            </div>
            <ResourcesMetaInfo resources={experiment.resources} />
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
              <GridTable values={experiment.declarations}/>
            </div>
            }
            {experiment.last_metric &&
            <div className="meta meta-metrics">
              <span className="meta-info">
                <i className="fa fa-area-chart icon" aria-hidden="true"/>
                <span className="title">Metrics:</span>
              </span>
              <GridTable values={experiment.last_metric}/>
            </div>
            }
          </div>
        </div>
      </div>
    );
  }
}
