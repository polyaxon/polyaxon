import * as React from 'react';
import * as _ from 'lodash';

import { GroupModel } from '../models/group';
import Status from './status';
import Description from './description';
import Tags from './tags';
import MetaInfo from './metaInfo/metaInfo';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import UserMetaInfo from './metaInfo/userMetaInfo';

export interface Props {
  group: GroupModel;
}

export default class GroupOverview extends React.Component<Props, Object> {
  public render() {
    const group = this.props.group;
    if (_.isNil(group)) {
      return (<div>Nothing</div>);
    }
    return (
      <div className="entity-details">
        <div className="row">
          <div className="col-md-12">
            <Description
              description={group.description}
              showEmpty={true}
            />
            <div className="meta">
              <UserMetaInfo user={group.user} inline={true}/>
              <DatesMetaInfo
                createdAt={group.created_at}
                updatedAt={group.updated_at}
                inline={true}
              />
            </div>
            <div className="meta">
              <TaskRunMetaInfo startedAt={group.started_at} finishedAt={group.finished_at} inline={true}/>
              <Status status={group.last_status}/>
            </div>
            <div className="meta">
              <MetaInfo
                icon="fa-asterisk"
                name="Algorithm"
                value={group.search_algorithm}
                inline={true}
              />
              <MetaInfo
                icon="fa-share-alt"
                name="Concurrency"
                value={group.concurrency}
                inline={true}
              />
              {group.current_iteration > 0 &&
              <MetaInfo
                icon="fa-refresh"
                name="Iteration"
                value={group.current_iteration}
                inline={true}
              />}
            </div>
            <div className="meta">
              <MetaInfo
                icon="fa-cube"
                name="Experiments"
                value={group.num_experiments}
                inline={true}
              />
              <MetaInfo
                icon="fa-hourglass-1"
                name="Scheduled"
                value={group.num_scheduled_experiments}
                inline={true}
              />
              <MetaInfo
                icon="fa-hourglass-end"
                name="Pending"
                value={group.num_pending_experiments}
                inline={true}
              />
              <MetaInfo
                icon="fa-bolt"
                name="Running"
                value={group.num_running_experiments}
                inline={true}
              />
              <MetaInfo
                icon="fa-check"
                name="Succeeded"
                value={group.num_succeeded_experiments}
                inline={true}
              />
              <MetaInfo
                icon="fa-close"
                name="Failed"
                value={group.num_failed_experiments}
                inline={true}
              />
              <MetaInfo
                icon="fa-stop"
                name="Stopped"
                value={group.num_stopped_experiments}
                inline={true}
              />
            </div>
            <Tags tags={group.tags}/>
          </div>
        </div>
      </div>
    );
  }
}
