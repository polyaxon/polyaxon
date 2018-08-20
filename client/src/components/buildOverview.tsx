import * as _ from 'lodash';
import * as React from 'react';

import { BuildModel } from '../models/build';
import Description from './description';
import { EmptyList } from './empty/emptyList';
import CommitMetaInfo from './metaInfo/commitMetaInfo';
import ExperimentCountMetaInfo from './metaInfo/counts/experimentCountMetaInfo';
import JobCountMetaInfo from './metaInfo/counts/jobCountMetaInfo';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import NodeMetaInfo from './metaInfo/nodeMetaInfo';
import ResourcesMetaInfo from './metaInfo/resourcesMetaInfo';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import UserMetaInfo from './metaInfo/userMetaInfo';
import Status from './status';
import Tags from './tags';

export interface Props {
  build: BuildModel;
}

export default class BuildOverview extends React.Component<Props, Object> {
  public render() {
    const build = this.props.build;

    if (_.isNil(build)) {
      return EmptyList(false, 'build', 'build');
    }
    return (
      <div className="entity-details">
        <div className="row">
          <div className="col-md-12">
             <Description
                description={build.description}
                showEmpty={true}
             />
            <div className="meta">
              <UserMetaInfo user={build.user} inline={true}/>
              <DatesMetaInfo
                createdAt={build.created_at}
                updatedAt={build.updated_at}
                inline={true}
              />
            </div>
            <div className="meta">
              <CommitMetaInfo commit={build.commit} inline={true}/>
              <NodeMetaInfo node={build.node_scheduled} inline={true}/>
            </div>
            <div className="meta">
              <TaskRunMetaInfo startedAt={build.started_at} finishedAt={build.finished_at} inline={true}/>
              <Status status={build.last_status}/>
            </div>
            <div className="meta">
              <ExperimentCountMetaInfo count={build.num_experiments} inline={true}/>
              <JobCountMetaInfo count={build.num_jobs} inline={true}/>
            </div>
            <ResourcesMetaInfo resources={build.resources} />
            <Tags tags={build.tags}/>
          </div>
        </div>
      </div>
    );
  }
}
