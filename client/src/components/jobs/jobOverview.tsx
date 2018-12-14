import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/job';
import { JobModel } from '../../models/job';
import { getJobCloning } from '../../utils/cloning';
import Description from '../description';
import { EmptyList } from '../empty/emptyList';
import MDEditor from '../mdEditor/mdEditor';
import CloningLinkMetaInfo from '../metaInfo/cloningLinkMetaInfo';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import NodeMetaInfo from '../metaInfo/nodeMetaInfo';
import ResourcesMetaInfo from '../metaInfo/resourcesMetaInfo';
import TaskRunMetaInfo from '../metaInfo/taskRunMetaInfo';
import UserMetaInfo from '../metaInfo/userMetaInfo';
import Name from '../name';
import Refresh from '../refresh';
import Status from '../status';
import Tags from '../tags';

export interface Props {
  job: JobModel;
  onUpdate: (updateDict: { [key: string]: any }) => actions.JobAction;
  onFetch: () => actions.JobAction;
}

export default class JobOverview extends React.Component<Props, {}> {
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
              <div className="col-md-11">
                <Description
                  description={job.description}
                  showEmpty={true}
                  onSave={(description: string) =>  { this.props.onUpdate({description}); }}
                />
              </div>
              <div className="col-md-1">
                <Refresh callback={this.refresh} pullRight={false}/>
              </div>
            </div>
            <div className="row">
              <div className="col-md-11">
                <Name
                  name="Group Name"
                  value={job.name || job.unique_name}
                  icon="fa-tasks"
                  onSave={(name: string) =>  { this.props.onUpdate({name}); }}
                />
              </div>
            </div>
            <div className="meta">
              <UserMetaInfo user={job.user} inline={true}/>
              <DatesMetaInfo
                createdAt={job.created_at}
                updatedAt={job.updated_at}
                inline={true}
              />
              {job.original &&
              <CloningLinkMetaInfo
                cloning={getJobCloning(job.original, job.cloning_strategy)}
                inline={true}
              />
              }
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
            <ResourcesMetaInfo resources={job.resources}/>
            <Tags
              tags={job.tags}
              onSave={(tags: string[]) =>  { this.props.onUpdate({tags}); }}
            />
            <MDEditor
              content={job.readme}
              onSave={(readme: string) => { this.props.onUpdate({readme}); }}
            />
          </div>
        </div>
      </div>
    );
  }
}
