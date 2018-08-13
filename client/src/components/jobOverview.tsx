import * as React from 'react';
import * as _ from 'lodash';

import { JobModel } from '../models/job';
import Status from './status';
import Description from './description';
import UserMetaInfo from './metaInfo/userMetaInfo';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import NodeMetaInfo from './metaInfo/nodeMetaInfo';
import ResourcesMetaInfo from './metaInfo/resourcesMetaInfo';
import Tags from './tags';
import { EmptyList } from './empty/emptyList';

export interface Props {
  job: JobModel;
}

export default class JobOverview extends React.Component<Props, Object> {
  public render() {
    const job = this.props.job;

    if (_.isNil(job)) {
      return EmptyList(false, 'job', 'job');
    }
    return (
      <div className="entity-details">
        <div className="row">
          <div className="col-md-12">
             <Description
                description={job.description}
                showEmpty={true}
             />
            <div className="meta">
              <UserMetaInfo user={job.user} inline={true}/>
              <DatesMetaInfo
                createdAt={job.created_at}
                updatedAt={job.updated_at}
                inline={true}
              />
            </div>
            <div className="meta">
              <NodeMetaInfo
                node={job.node_scheduled}
                inline={true}
              />
            </div>
            <div className="meta">
              <TaskRunMetaInfo startedAt={job.started_at} finishedAt={job.finished_at} inline={true}/>
              <Status status={job.last_status}/>
            </div>
            <ResourcesMetaInfo resources={job.resources} />
            <Tags tags={job.tags}/>
          </div>
        </div>
      </div>
    );
  }
}
