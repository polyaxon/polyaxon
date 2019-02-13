import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import * as actions from '../../actions/group';
import { isDone } from '../../constants/statuses';
import { getGroupUrl, splitUniqueName } from '../../constants/utils';
import { BookmarkInterface } from '../../interfaces/bookmarks';
import { GroupModel } from '../../models/group';
import { getBookmark } from '../../utils/bookmarks';
import BookmarkStar from '../bookmarkStar';
import Description from '../description';
import ConcurrencyMetaInfo from '../metaInfo/concurrencyMetaInfo';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import GroupType from '../metaInfo/groupType';
import IdMetaInfo from '../metaInfo/idMetaInfo';
import SearchAlgorithmMetaInfo from '../metaInfo/searchAlgorithmMetaInfo';
import TaskRunMetaInfo from '../metaInfo/taskRunMetaInfo';
import UserMetaInfo from '../metaInfo/userMetaInfo';
import Status from '../status';
import Tags from '../tags';
import GroupActions from './groupActions';

export interface Props {
  group: GroupModel;
  onDelete: () => actions.GroupAction;
  onStop: () => actions.GroupAction;
  onArchive: () => actions.GroupAction;
  onRestore: () => actions.GroupAction;
  showBookmarks: boolean;
  bookmark: () => actions.GroupAction;
  unbookmark: () => actions.GroupAction;
}

function Group({
                 group,
                 onDelete,
                 onStop,
                 onArchive,
                 onRestore,
                 bookmark,
                 unbookmark,
                 showBookmarks}: Props) {
  const values = splitUniqueName(group.project);
  const bookmarkStar: BookmarkInterface = getBookmark(
    group.bookmarked, bookmark, unbookmark);

  return (
    <tr className="list-item">
      <td className="block">
        <Status status={group.last_status}/>
      </td>
      <td className="block">
        <LinkContainer to={getGroupUrl(values[0], values[1], group.id)}>
          <a className="title">
            <i className="fa fa-cubes icon" aria-hidden="true"/>
            {group.name || group.unique_name}
          </a>
        </LinkContainer>
        {showBookmarks &&
        <BookmarkStar active={bookmarkStar.active} callback={bookmarkStar.callback}/>
        }
        <Description description={group.description}/>
        <div className="meta">
          <IdMetaInfo value={group.id} inline={true}/>
          <UserMetaInfo user={group.user} inline={true}/>
          <DatesMetaInfo
            createdAt={group.created_at}
            updatedAt={group.updated_at}
            inline={true}
          />
        </div>
        <Tags tags={group.tags}/>
      </td>
      {group.group_type === 'selection'
        ? <td className="block">
            <GroupType groupTyp={group.group_type}/>
          </td>
        : <td className="block">
            <GroupType groupTyp={group.group_type}/>
            <SearchAlgorithmMetaInfo searchAlgorithm={group.search_algorithm}/>
            <ConcurrencyMetaInfo concurrency={group.concurrency}/>
          </td>
      }
      {group.group_type === 'selection'
        ? <td className="block">
            N/A
          </td>
        : <td className="block">
            <TaskRunMetaInfo startedAt={group.started_at} finishedAt={group.finished_at}/>
          </td>
      }
      <td className="block pull-right">
        <GroupActions
          onDelete={onDelete}
          onStop={group.group_type === 'study' ? onStop : undefined}
          onArchive={group.deleted ? undefined : onArchive}
          onRestore={group.deleted ? onRestore : undefined}
          isRunning={!isDone(group.last_status)}
          pullRight={false}
        />
      </td>
    </tr>
  );
}

export default Group;
