import * as _ from 'lodash';
import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import { isDone } from '../constants/statuses';
import { getJobUrl, splitUniqueName } from '../constants/utils';
import { getBuildUrl } from '../constants/utils';
import { JobModel } from '../models/job';
import Actions from './actions';
import Description from './description';
import BuildLinkMetaInfo from './metaInfo/buildLinkMetaInfo';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import UserMetaInfo from './metaInfo/userMetaInfo';
import Status from './status';
import Tags from './tags';

export interface Props {
  job: JobModel;
  onDelete: () => void;
  onStop: () => void;
}

function Job({job, onDelete, onStop}: Props) {
  const values = splitUniqueName(job.project);
  let buildUrl = '';
  let buildValues: string[] = [];
  if (!_.isNil(job.build_job)) {
    buildValues = splitUniqueName(job.build_job);
    buildUrl = getBuildUrl(buildValues[0], buildValues[1], buildValues[3]);
  }

  return (
    <tr className="list-item">
      <td className="block">
        <Status status={job.last_status}/>
      </td>
      <td className="block">
        <LinkContainer to={getJobUrl(values[0], values[1], job.id)}>
          <a className="title">
            <i className="fa fa-tasks icon" aria-hidden="true"/>
            {job.unique_name}
          </a>
        </LinkContainer>
        <Description description={job.description}/>
        <div className="meta">
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
      </td>
      <td className="block">
        <TaskRunMetaInfo startedAt={job.started_at} finishedAt={job.finished_at}/>
      </td>
      <td className="block">
        <Actions
          onDelete={onDelete}
          onStop={onStop}
          isRunning={!isDone(job.last_status)}
        />
      </td>
    </tr>
  );
}

export default Job;
