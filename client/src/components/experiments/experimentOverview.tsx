import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/experiment';
import { getExperimentTensorboardUrl } from '../../constants/utils';
import { ExperimentModel } from '../../models/experiment';
import Description from '../description';
import { EmptyList } from '../empty/emptyList';
import MDEditor from '../mdEditor/mdEditor';
import JobCountMetaInfo from '../metaInfo/counts/jobCountMetaInfo';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import ResourcesMetaInfo from '../metaInfo/resourcesMetaInfo';
import TaskRunMetaInfo from '../metaInfo/taskRunMetaInfo';
import UserMetaInfo from '../metaInfo/userMetaInfo';
import Status from '../status';
import VerticalTable from '../tables/verticalTable';
import Tags from '../tags';

export interface Props {
  experiment: ExperimentModel;
  onUpdate: (updateDict: { [key: string]: any }) => actions.ExperimentAction;
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
              onSave={(description: string) =>  { this.props.onUpdate({description}); }}
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
            <ResourcesMetaInfo resources={experiment.resources}/>
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
            <Tags
              tags={experiment.tags}
              onSave={(tags: string[]) =>  { this.props.onUpdate({tags}); }}
            />
            {experiment.declarations &&
            <div className="row">
              <div className="col-md-8">
                <div className="meta meta-declarations">
                  <span className="meta-info">
                    <i className="fa fa-gear icon" aria-hidden="true"/>
                    <span className="title">Declarations:</span>
                  </span>
                  <VerticalTable values={experiment.declarations}/>
                </div>
              </div>
            </div>
            }
            {experiment.last_metric &&
            <div className="row">
              <div className="col-md-8">
                <div className="meta meta-metrics">
                <span className="meta-info">
                  <i className="fa fa-area-chart icon" aria-hidden="true"/>
                  <span className="title">Metrics:</span>
                </span>
                  <VerticalTable values={experiment.last_metric}/>
                </div>
              </div>
            </div>
            }
            {experiment.data_refs &&
            <div className="row">
              <div className="col-md-8">
                <div className="meta meta-data-refs">
              <span className="meta-info">
                <i className="fa fa-database icon" aria-hidden="true"/>
                <span className="title">Data refs:</span>
              </span>
                  <VerticalTable values={experiment.data_refs}/>
                </div>
              </div>
            </div>
            }
            <MDEditor
              content={experiment.readme}
              onSave={(readme: string) => { this.props.onUpdate({readme}); }}
            />
          </div>
        </div>
      </div>
    );
  }
}
