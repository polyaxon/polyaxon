import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import * as actions from '../../actions/tensorboard';
import { isDone } from '../../constants/statuses';
import {
  getTensorboardApiUrl,
  splitUniqueName
} from '../../constants/utils';
import { BookmarkInterface } from '../../interfaces/bookmarks';
import { TensorboardModel } from '../../models/tensorboard';
import { getBookmark } from '../../utils/bookmarks';
import BookmarkStar from '../bookmarkStar';
import Description from '../description';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import IdMetaInfo from '../metaInfo/idMetaInfo';
import NodeMetaInfo from '../metaInfo/nodeMetaInfo';
import PodIdMetaInfo from '../metaInfo/podIdMetaInfo';
import TaskRunMetaInfo from '../metaInfo/taskRunMetaInfo';
import TensorboardInfoMetaInfo from '../metaInfo/tensorboardInfoMetaInfo';
import UserMetaInfo from '../metaInfo/userMetaInfo';
import Status from '../status';
import Tags from '../tags';
import TensorboardActions from './tensorboardActions';

export interface Props {
  tensorboard: TensorboardModel;
  onDelete: () => actions.TensorboardAction;
  onStop: () => actions.TensorboardAction;
  onArchive: () => actions.TensorboardAction;
  onRestore: () => actions.TensorboardAction;
  showBookmarks: boolean;
  bookmark: () => actions.TensorboardAction;
  unbookmark: () => actions.TensorboardAction;
}

function Tensorboard({
                      tensorboard,
                      onDelete,
                      onStop,
                      onArchive,
                      onRestore,
                      bookmark,
                      unbookmark,
                      showBookmarks
                    }: Props) {
  const values = splitUniqueName(tensorboard.project);
  const bookmarkStar: BookmarkInterface = getBookmark(
    tensorboard.bookmarked, bookmark, unbookmark);

  return (
    <tr className="list-item">
      <td className="block">
        <Status status={tensorboard.last_status}/>
      </td>
      <td className="block">
        <LinkContainer to={getTensorboardApiUrl(values[0], values[1], tensorboard.id)}>
          <a className="title">
            <i className="fa fa-gavel icon" aria-hidden="true"/>
            {tensorboard.name || tensorboard.unique_name}
          </a>
        </LinkContainer>
        {showBookmarks &&
        <BookmarkStar active={bookmarkStar.active} callback={bookmarkStar.callback}/>
        }
        <Description description={tensorboard.description}/>
        <div className="meta">
          <PodIdMetaInfo value={tensorboard.pod_id} inline={true}/>
        </div>
        <div className="meta">
          <NodeMetaInfo node={tensorboard.node_scheduled} inline={true}/>
        </div>
        <div className="meta">
          <IdMetaInfo value={tensorboard.id} inline={true}/>
          <UserMetaInfo user={tensorboard.user} inline={true}/>
          <DatesMetaInfo
            createdAt={tensorboard.created_at}
            updatedAt={tensorboard.updated_at}
            inline={true}
          />
        </div>
        <Tags tags={tensorboard.tags}/>
      </td>
      <td className="block">
        <TensorboardInfoMetaInfo
          username={values[0]}
          projectName={values[1]}
          project={tensorboard.project}
          experiment={tensorboard.experiment}
          group={tensorboard.group}
          inline={false}
        />
      </td>
      <td className="block">
        <TaskRunMetaInfo startedAt={tensorboard.started_at} finishedAt={tensorboard.finished_at}/>
      </td>
      <td className="block pull-right">
        <TensorboardActions
          onDelete={onDelete}
          onStop={onStop}
          onArchive={tensorboard.deleted ? undefined : onArchive}
          onRestore={tensorboard.deleted ? onRestore : undefined}
          isRunning={!isDone(tensorboard.last_status)}
          pullRight={false}
        />
      </td>
    </tr>
  );
}

export default Tensorboard;
