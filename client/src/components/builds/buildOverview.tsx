import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/build';
import { BuildModel } from '../../models/build';
import Description from '../description';
import { EmptyList } from '../empty/emptyList';
import BuildBackendMetaInfo from '../metaInfo/BuildBackendMetaInfo';
import CommitMetaInfo from '../metaInfo/commitMetaInfo';
import ExperimentCountMetaInfo from '../metaInfo/counts/experimentCountMetaInfo';
import JobCountMetaInfo from '../metaInfo/counts/jobCountMetaInfo';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import NodeMetaInfo from '../metaInfo/nodeMetaInfo';
import PodIdMetaInfo from '../metaInfo/podIdMetaInfo';
import ResourcesMetaInfo from '../metaInfo/resourcesMetaInfo';
import TaskRunMetaInfo from '../metaInfo/taskRunMetaInfo';
import UserMetaInfo from '../metaInfo/userMetaInfo';
import Name from '../name';
import Refresh from '../refresh';
import Status from '../status';
import Tags from '../tags';

export interface Props {
  build: BuildModel;
  onUpdate: (updateDict: { [key: string]: any }) => actions.BuildAction;
  onFetch: () => actions.BuildAction;
}

export default class BuildOverview extends React.Component<Props, {}> {
  public refresh = () => {
    this.props.onFetch();
  };

  public render() {
    const build = this.props.build;

    if (_.isNil(build)) {
      return EmptyList(false, 'build', 'build');
    }
    return (
      <div className="entity-details">
        <div className="row">
          <div className="col-md-12">
            <div className="row">
              <div className="col-md-11">
                <Description
                  description={build.description}
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
                  name="Build Name"
                  value={build.name || build.unique_name}
                  icon="fa-gavel"
                  onSave={(name: string) =>  { this.props.onUpdate({name}); }}
                />
              </div>
            </div>
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
              <BuildBackendMetaInfo value={build.backend} inline={true}/>
            </div>
            <div className="meta">
              <PodIdMetaInfo value={build.pod_id} inline={true}/>
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
            <ResourcesMetaInfo resources={build.resources}/>
            <Tags
              tags={build.tags}
              onSave={(tags: string[]) =>  { this.props.onUpdate({tags}); }}
            />
          </div>
        </div>
      </div>
    );
  }
}
