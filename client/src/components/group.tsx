import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import { isDone } from '../constants/statuses';
import {
  getGroupUrl,
  splitUniqueName
} from '../constants/utils';
import { GroupModel } from '../models/group';
import Actions from './actions';
import Description from './description';
import ConcurrencyMetaInfo from './metaInfo/concurrencyMetaInfo';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import SearchAlgorithmMetaInfo from './metaInfo/searchAlgorithmMetaInfo';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import UserMetaInfo from './metaInfo/userMetaInfo';
import Status from './status';
import Tags from './tags';

export interface Props {
  group: GroupModel;
  onDelete: () => void;
  onStop: () => void;
}

function Group({group, onDelete, onStop}: Props) {
  const values = splitUniqueName(group.project);

  return (
    <tr className="list-item">
      <td className="block">
        <Status status={group.last_status}/>
      </td>
      <td className="block">
        <LinkContainer to={getGroupUrl(values[0], values[1], group.id)}>
          <a className="title">
            <i className="fa fa-cubes icon" aria-hidden="true"/>
            {group.unique_name}
          </a>
        </LinkContainer>
        <Description description={group.description}/>
        <div className="meta">
          <UserMetaInfo user={group.user} inline={true}/>
          <DatesMetaInfo
            createdAt={group.created_at}
            updatedAt={group.updated_at}
            inline={true}
          />
        </div>
        <Tags tags={group.tags}/>
      </td>
      <td className="block">
        <SearchAlgorithmMetaInfo searchAlgorithm={group.search_algorithm}/>
        <ConcurrencyMetaInfo concurrency={group.concurrency}/>
      </td>
      <td className="block">
        <TaskRunMetaInfo startedAt={group.started_at} finishedAt={group.finished_at}/>
      </td>
      <td className="block pull-right">
        <Actions
          onDelete={onDelete}
          onStop={onStop}
          isRunning={!isDone(group.last_status)}
        />
      </td>
    </tr>
  );
}

export default Group;
