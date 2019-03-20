import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/tensorboard';
import { splitUniqueName } from '../../constants/utils';
import { TensorboardModel } from '../../models/tensorboard';
import Description from '../description';
import { EmptyList } from '../empty/emptyList';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import NodeMetaInfo from '../metaInfo/nodeMetaInfo';
import PodIdMetaInfo from '../metaInfo/podIdMetaInfo';
import ResourcesMetaInfo from '../metaInfo/resourcesMetaInfo';
import TaskRunMetaInfo from '../metaInfo/taskRunMetaInfo';
import TensorboardInfoMetaInfo from '../metaInfo/tensorboardInfoMetaInfo';
import UserMetaInfo from '../metaInfo/userMetaInfo';
import Name from '../name';
import Refresh from '../refresh';
import Status from '../statuses/status';
import Tags from '../tags/tags';

export interface Props {
  tensorboard: TensorboardModel;
  onUpdate: (updateDict: { [key: string]: any }) => actions.TensorboardAction;
  onFetch: () => actions.TensorboardAction;
}

export default class TensorboardOverview extends React.Component<Props, {}> {
  public refresh = () => {
    this.props.onFetch();
  };

  public render() {
    const tensorboard = this.props.tensorboard;
    const values = splitUniqueName(tensorboard.project);

    if (_.isNil(tensorboard)) {
      return EmptyList(false, 'tensorboard', 'tensorboard');
    }
    return (
      <div className="entity-details">
        <div className="row">
          <div className="col-md-12">
            <div className="row">
              <div className="col-md-11">
                <Description
                  description={tensorboard.description}
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
                  name="Tensorboard Name"
                  value={tensorboard.name || tensorboard.unique_name}
                  icon="fas fa-gavel"
                  onSave={(name: string) =>  { this.props.onUpdate({name}); }}
                />
              </div>
            </div>
            <div className="meta">
              <UserMetaInfo user={tensorboard.user} inline={true}/>
              <DatesMetaInfo
                createdAt={tensorboard.created_at}
                updatedAt={tensorboard.updated_at}
                inline={true}
              />
            </div>
            <div className="meta">
              <TensorboardInfoMetaInfo
                username={values[0]}
                projectName={values[1]}
                project={tensorboard.project}
                experiment={tensorboard.experiment}
                group={tensorboard.group}
                inline={true}
              />
            </div>
            <div className="meta">
              <PodIdMetaInfo value={tensorboard.pod_id} inline={true}/>
              <NodeMetaInfo node={tensorboard.node_scheduled} inline={true}/>
            </div>
            <div className="meta">
              <TaskRunMetaInfo startedAt={tensorboard.started_at} finishedAt={tensorboard.finished_at} inline={true}/>
              <Status status={tensorboard.last_status}/>
            </div>
            <ResourcesMetaInfo resources={tensorboard.resources}/>
            <Tags
              tags={tensorboard.tags}
              onSave={(tags: string[]) =>  { this.props.onUpdate({tags}); }}
            />
          </div>
        </div>
      </div>
    );
  }
}
