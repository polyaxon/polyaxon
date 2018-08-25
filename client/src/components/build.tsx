import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import { isDone } from '../constants/statuses';
import { getBuildUrl, splitUniqueName } from '../constants/utils';
import { BuildModel } from '../models/build';
import Actions from './actions';
import Description from './description';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import UserMetaInfo from './metaInfo/userMetaInfo';
import Status from './status';
import Tags from './tags';

export interface Props {
  build: BuildModel;
  onDelete: () => void;
  onStop: () => void;
}

function Build({build, onDelete, onStop}: Props) {
  const values = splitUniqueName(build.project);

  return (
    <tr className="list-item">
      <td className="block">
        <Status status={build.last_status}/>
      </td>
      <td className="block">
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
      </td>
      <td className="block">
        <TaskRunMetaInfo startedAt={build.started_at} finishedAt={build.finished_at}/>
      </td>
      <td className="block pull-right">
        <Actions
          onDelete={onDelete}
          onStop={onStop}
          isRunning={!isDone(build.last_status)}
        />
      </td>
    </tr>
  );
}

export default Build;
