import * as React from 'react';
import * as _ from 'lodash';
import { LinkContainer } from 'react-router-bootstrap';

import { JobModel } from '../models/job';
import Status from './status';
import Description from './description';
import Tags from './tags';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import UserMetaInfo from './metaInfo/userMetaInfo';
import LinkMetaInfo from './metaInfo/linkMetaInfo';
import { getJobUrl, splitUniqueName } from '../constants/utils';
import { getBuildUrl } from '../constants/utils';

export interface Props {
  job: JobModel;
  onDelete: () => void;
}

function Job({job, onDelete}: Props) {
  let values = splitUniqueName(job.project);
  let buildUrl = '';
  let buildValues: string[] = [];
  if (!_.isNil(job.build_job)) {
    buildValues = splitUniqueName(job.build_job);
    buildUrl = getBuildUrl(buildValues[0], buildValues[1], buildValues[3]);
  }

  return (
    <div className="row">
      <div className="col-md-1 block">
        <Status status={job.last_status}/>
      </div>
      <div className="col-md-7 block">
        <LinkContainer to={getJobUrl(values[0], values[1], job.id)}>
          <a className="title">
            <i className="fa fa-cubes icon" aria-hidden="true"/>
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
      </div>
      <div className="col-md-2 block">
        <LinkMetaInfo
          icon="fa-cog"
          name="Build"
          value={buildValues[3]}
          link={buildUrl}
        />
      </div>
      <div className="col-md-2 block">
        <TaskRunMetaInfo startedAt={job.created_at} finishedAt={job.updated_at}/>
      </div>
    </div>
  );
}

export default Job;
