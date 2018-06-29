import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import { BuildModel } from '../models/build';
import Status from './status';
import Description from './description';
import Tags from './tags';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import UserMetaInfo from './metaInfo/userMetaInfo';
import { getBuildUrl, splitUniqueName } from '../constants/utils';

export interface Props {
  build: BuildModel;
  onDelete: () => void;
}

function Build({build, onDelete}: Props) {
  let values = splitUniqueName(build.project);

  return (
    <div className="row">
      <div className="col-md-1 block">
        <Status status={build.last_status}/>
      </div>
      <div className="col-md-9 block">
        <LinkContainer to={getBuildUrl(values[0], values[1], build.id)}>
          <a className="title">
            <i className="fa fa-gavel icon" aria-hidden="true"/>
            {build.unique_name}
          </a>
        </LinkContainer>
        <Description description={build.description}/>
        <div className="meta">
          <UserMetaInfo user={build.user} inline={true}/>
          <DatesMetaInfo
            createdAt={build.created_at}
            updatedAt={build.updated_at}
            inline={true}
          />
        </div>
        <Tags tags={build.tags}/>
      </div>
      <div className="col-md-2 block">
        <TaskRunMetaInfo startedAt={build.created_at} finishedAt={build.updated_at}/>
      </div>
    </div>
  );
}

export default Build;
