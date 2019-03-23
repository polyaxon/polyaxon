import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/notebooks';
import { NotebookModel } from '../../models/notebook';
import Description from '../description';
import { EmptyList } from '../empty/emptyList';
import BackendMetaInfo from '../metaInfo/backendMetaInfo';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import NodeMetaInfo from '../metaInfo/nodeMetaInfo';
import NotebookTargetMetaInfo from '../metaInfo/notebookTargetMetaInfo';
import PodIdMetaInfo from '../metaInfo/podIdMetaInfo';
import ResourcesMetaInfo from '../metaInfo/resourcesMetaInfo';
import TaskRunMetaInfo from '../metaInfo/taskRunMetaInfo';
import UserMetaInfo from '../metaInfo/userMetaInfo';
import Name from '../name';
import Refresh from '../refresh';
import Status from '../statuses/status';
import Tags from '../tags/tags';

export interface Props {
  notebook: NotebookModel;
  onUpdate: (updateDict: { [key: string]: any }) => actions.NotebookAction;
  onFetch: () => actions.NotebookAction;
}

export default class NotebookOverview extends React.Component<Props, {}> {
  public refresh = () => {
    this.props.onFetch();
  };

  public render() {
    const notebook = this.props.notebook;

    if (_.isNil(notebook)) {
      return EmptyList(false, 'notebook', 'notebook');
    }
    return (
      <div className="entity-details">
        <div className="row">
          <div className="col-md-12">
            <div className="row">
              <div className="col-md-11">
                <Description
                  description={notebook.description}
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
                  name="Notebook Name"
                  value={notebook.name || notebook.unique_name}
                  icon="fas fa-gavel"
                  onSave={(name: string) =>  { this.props.onUpdate({name}); }}
                />
              </div>
            </div>
            <div className="meta">
              <UserMetaInfo user={notebook.user} inline={true}/>
              <DatesMetaInfo
                createdAt={notebook.created_at}
                updatedAt={notebook.updated_at}
                inline={true}
              />
            </div>
            <div className="meta">
              <BackendMetaInfo value={notebook.backend} inline={true}/>
              <NotebookTargetMetaInfo project={notebook.project} inline={true}/>
            </div>
            <div className="meta">
              <PodIdMetaInfo value={notebook.pod_id} inline={true}/>
              <NodeMetaInfo node={notebook.node_scheduled} inline={true}/>
            </div>
            <div className="meta">
              <TaskRunMetaInfo startedAt={notebook.started_at} finishedAt={notebook.finished_at} inline={true}/>
              <Status status={notebook.last_status}/>
            </div>
            <ResourcesMetaInfo resources={notebook.resources}/>
            <Tags
              tags={notebook.tags}
              onSave={(tags: string[]) =>  { this.props.onUpdate({tags}); }}
            />
          </div>
        </div>
      </div>
    );
  }
}
