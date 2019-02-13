import * as _ from 'lodash';
import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import * as actions from '../../actions/job';
import { isDone } from '../../constants/statuses';
import { getBuildUrl, getJobUrl, splitUniqueName } from '../../constants/utils';
import { BookmarkInterface } from '../../interfaces/bookmarks';
import { JobModel } from '../../models/job';
import { getBookmark } from '../../utils/bookmarks';
import { getJobCloning } from '../../utils/cloning';
import BookmarkStar from '../bookmarkStar';
import Description from '../description';
import BuildLinkMetaInfo from '../metaInfo/buildLinkMetaInfo';
import CloningLinkMetaInfo from '../metaInfo/cloningLinkMetaInfo';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import IdMetaInfo from '../metaInfo/idMetaInfo';
import PodIdMetaInfo from '../metaInfo/podIdMetaInfo';
import TaskRunMetaInfo from '../metaInfo/taskRunMetaInfo';
import UserMetaInfo from '../metaInfo/userMetaInfo';
import Status from '../status';
import Tags from '../tags';
import JobActions from './jobActions';

export interface Props {
  job: JobModel;
  onDelete: () => actions.JobAction;
  onStop: () => actions.JobAction;
  onArchive: () => actions.JobAction;
  onRestore: () => actions.JobAction;
  showBookmarks: boolean;
  bookmark: () => actions.JobAction;
  unbookmark: () => actions.JobAction;
}

function Job({
               job,
               onDelete,
               onStop,
               onArchive,
               onRestore,
               bookmark,
               unbookmark,
               showBookmarks
             }: Props) {
  const values = splitUniqueName(job.project);
  let buildUrl = '';
  let buildValues: string[] = [];
  if (!_.isNil(job.build_job)) {
    buildValues = splitUniqueName(job.build_job);
    buildUrl = getBuildUrl(buildValues[0], buildValues[1], buildValues[3]);
  }
  const bookmarkStar: BookmarkInterface = getBookmark(
    job.bookmarked, bookmark, unbookmark);

  return (
    <tr className="list-item">
      <td className="block">
        <Status status={job.last_status}/>
      </td>
      <td className="block">
        <LinkContainer to={getJobUrl(values[0], values[1], job.id)}>
          <a className="title">
            <i className="fa fa-tasks icon" aria-hidden="true"/>
            {job.name || job.unique_name}
          </a>
        </LinkContainer>
        {showBookmarks &&
        <BookmarkStar active={bookmarkStar.active} callback={bookmarkStar.callback}/>
        }
        <Description description={job.description}/>
        <div className="meta">
          <PodIdMetaInfo value={job.pod_id} inline={true}/>
        </div>
        <div className="meta">
          <IdMetaInfo value={job.id} inline={true}/>
          <UserMetaInfo user={job.user} inline={true}/>
          <DatesMetaInfo
            createdAt={job.created_at}
            updatedAt={job.updated_at}
            inline={true}
          />
        </div>
        <Tags tags={job.tags}/>
      </td>
      <td className="block">
        <BuildLinkMetaInfo
          value={buildValues[3]}
          link={buildUrl}
        />
        {job.original &&
        <CloningLinkMetaInfo
          cloning={getJobCloning(job.original, job.cloning_strategy)}
        />
        }
      </td>
      <td className="block">
        <TaskRunMetaInfo startedAt={job.started_at} finishedAt={job.finished_at}/>
      </td>
      <td className="block pull-right">
        <JobActions
          onDelete={onDelete}
          onStop={onStop}
          onArchive={job.deleted ? undefined : onArchive}
          onRestore={job.deleted ? onRestore : undefined}
          isRunning={!isDone(job.last_status)}
          pullRight={false}
        />
      </td>
    </tr>
  );
}

export default Job;
