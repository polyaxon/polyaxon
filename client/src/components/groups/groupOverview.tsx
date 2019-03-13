import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/group';
import { getGroupTensorboardUrl } from '../../constants/utils';
import { GroupModel } from '../../models/group';
import Description from '../description';
import { EmptyList } from '../empty/emptyList';
import MDEditor from '../mdEditor/mdEditor';
import ConcurrencyMetaInfo from '../metaInfo/concurrencyMetaInfo';
import ExperimentCountMetaInfo from '../metaInfo/counts/experimentCountMetaInfo';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import GroupType from '../metaInfo/groupType';
import MetaInfo from '../metaInfo/metaInfo';
import SearchAlgorithmMetaInfo from '../metaInfo/searchAlgorithmMetaInfo';
import TaskRunMetaInfo from '../metaInfo/taskRunMetaInfo';
import UserMetaInfo from '../metaInfo/userMetaInfo';
import Name from '../name';
import Refresh from '../refresh';
import Status from '../status';
import Tags from '../tags';

export interface Props {
  group: GroupModel;
  onUpdate: (updateDict: { [key: string]: any }) => actions.GroupAction;
  onFetch: () => actions.GroupAction;
}

export default class GroupOverview extends React.Component<Props, {}> {
  public refresh = () => {
    this.props.onFetch();
  };

  public render() {
    const group = this.props.group;
    if (_.isNil(group)) {
      return EmptyList(false, 'experiment group', 'group');
    }
    return (
      <div className="entity-details">
        <div className="row">
          <div className="col-md-12">
            <div className="row">
              <div className="col-md-11">
                <Description
                  description={group.description}
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
                  value={group.name || group.unique_name}
                  icon="fas fa-cubes"
                  onSave={(name: string) =>  { this.props.onUpdate({name}); }}
                />
              </div>
            </div>
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
            {group.group_type === 'study'
              ? <div className="meta">
                <GroupType groupTyp={group.group_type} inline={true}/>
                <SearchAlgorithmMetaInfo
                  searchAlgorithm={group.search_algorithm}
                  inline={true}
                />
                <ConcurrencyMetaInfo
                  concurrency={group.concurrency}
                  inline={true}
                />
                {group.current_iteration > 0 &&
                <MetaInfo
                  icon="fas fa-sync-alt"
                  name="Iteration"
                  value={group.current_iteration}
                  inline={true}
                />}
              </div>
              : <div className="meta">
                  <GroupType groupTyp={group.group_type} inline={true}/>
                </div>
            }
            <div className="meta">
              <ExperimentCountMetaInfo
                count={group.num_experiments}
                inline={true}
              />
              <MetaInfo
                icon="fas fa-hourglass-start"
                name="Scheduled"
                value={group.num_scheduled_experiments}
                inline={true}
              />
              <MetaInfo
                icon="fas fa-hourglass-end"
                name="Pending"
                value={group.num_pending_experiments}
                inline={true}
              />
              <MetaInfo
                icon="fas fa-bolt"
                name="Running"
                value={group.num_running_experiments}
                inline={true}
              />
              <MetaInfo
                icon="fas fa-check"
                name="Succeeded"
                value={group.num_succeeded_experiments}
                inline={true}
              />
              <MetaInfo
                icon="fas fa-times"
                name="Failed"
                value={group.num_failed_experiments}
                inline={true}
              />
              <MetaInfo
                icon="fas fa-stop"
                name="Stopped"
                value={group.num_stopped_experiments}
                inline={true}
              />
            </div>
            {group.has_tensorboard &&
            <div className="meta">
              <span className="meta-info meta-dashboard">
                <i className="fas fa-link icon" aria-hidden="true"/>
                <a
                  href={getGroupTensorboardUrl(group.project, group.id)}
                  className="title-link"
                >Tensorboard
                </a>
              </span>
            </div>
            }
            <Tags
              tags={group.tags}
              onSave={(tags: string[]) =>  { this.props.onUpdate({tags}); }}
            />
            <MDEditor
              content={group.readme}
              onSave={(readme: string) => { this.props.onUpdate({readme}); }}
            />
          </div>
        </div>
      </div>
    );
  }
}
