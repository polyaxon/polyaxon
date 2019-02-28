import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/job';
import { ExperimentJobModel } from '../../models/experimentJob';
import { EmptyList } from '../empty/emptyList';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import IdMetaInfo from '../metaInfo/idMetaInfo';
import NodeMetaInfo from '../metaInfo/nodeMetaInfo';
import PodIdMetaInfo from '../metaInfo/podIdMetaInfo';
import ResourcesMetaInfo from '../metaInfo/resourcesMetaInfo';
import TaskRunMetaInfo from '../metaInfo/taskRunMetaInfo';
import UserMetaInfo from '../metaInfo/userMetaInfo';
import Name from '../name';
import Refresh from '../refresh';
import Status from '../status';

export interface Props {
  job: ExperimentJobModel;
  onFetch: () => actions.JobAction;
}

export default class ExperimentJobOverview extends React.Component<Props, {}> {
  public refresh = () => {
    this.props.onFetch();
  };

  public render() {
    const job = this.props.job;

    if (_.isNil(job)) {
      return EmptyList(false, 'job', 'job');
    }
    return (
      <div className="entity-details">
        <div className="row">
          <div className="col-md-12">
            <div className="row">
              <div className="col-md-offset-11 col-md-1">
                <Refresh callback={this.refresh} pullRight={false}/>
              </div>
            </div>
            <div className="row">
              <div className="col-md-11">
                <Name
                  name="Job Name"
                  value={job.name || job.unique_name}
                  icon="fa-tasks"
                />
              </div>
            </div>
            <div className="meta">
               <span className="meta-info">
                 <i className="fa fa-certificate icon" aria-hidden="true"/>
                 <span className="title">Role:</span>
                 {job.role}
               </span>
              <IdMetaInfo value={job.id} inline={true}/>
            </div>
            <div className="meta">
              <UserMetaInfo user={'user'} inline={true}/>
              <DatesMetaInfo
                createdAt={job.created_at}
                updatedAt={job.updated_at}
                inline={true}
              />
            </div>
            <div className="meta">
              <PodIdMetaInfo value={job.pod_id} inline={true}/>
              <NodeMetaInfo node={job.node_scheduled} inline={true}/>
            </div>
            <div className="meta">
              <TaskRunMetaInfo startedAt={job.started_at} finishedAt={job.finished_at} inline={true}/>
              <Status status={job.last_status}/>
            </div>
            <ResourcesMetaInfo resources={job.resources}/>
          </div>
        </div>
      </div>
    );
  }
}
