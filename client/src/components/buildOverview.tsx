import * as React from 'react';
import * as _ from 'lodash';

import { BuildModel } from '../models/build';
import Status from './status';
import Description from './description';
import UserMetaInfo from './metaInfo/userMetaInfo';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import MetaInfo from 'src/components/metaInfo/metaInfo';

export interface Props {
  build: BuildModel;
}

export default class BuildOverview extends React.Component<Props, Object> {
  public render() {
    const build = this.props.build;

    if (_.isNil(build)) {
      return (<div>Nothing</div>);
    }
    return (
      <div className="entity-details">
        <div className="row">
          <div className="col-md-12">
             <Description
                description={build.description}
                entity="build"
                command="polyaxon build update --description=..."
             />
            <div className="meta">
              <UserMetaInfo user={build.user} inline={true}/>
              <DatesMetaInfo
                createdAt={build.created_at}
                updatedAt={build.updated_at}
                inline={true}
              />
              <MetaInfo
                icon="fa-hashtag"
                name="Commit"
                value={build.commit}
                inline={true}
              />
            </div>
            <div className="meta">
              <TaskRunMetaInfo startedAt={build.started_at} finishedAt={build.finished_at} inline={true}/>
              <Status status={build.last_status}/>
            </div>
            {build.resources &&
            <div className="meta meta-resources">
              {Object.keys(build.resources)
                .filter(
                  (res, idx) =>
                    build.resources[res] != null
                )
                .map(
                  (res, idx) =>
                    <span className="meta-info" key={idx}>
                <i className="fa fa-microchip icon" aria-hidden="true"/>
                <span className="title">{res}:</span>
                      {build.resources[res].requests || ''} - {build.resources[res].limits || ''}
              </span>
                )}
            </div>
            }
            <Tags tags={group.tags}/>
          </div>
        </div>
      </div>
    );
  }
}
