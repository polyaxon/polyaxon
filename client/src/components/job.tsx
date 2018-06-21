import * as React from 'react';

import { JobModel } from '../models/job';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import Status from './status';

export interface Props {
  job: JobModel;
  onDelete: () => void;
}

function Job({job, onDelete}: Props) {
  let jobDetailUrl = `jobs/${job.id}/`;

  return (
    <div className="row">
      <div className="col-md-1 block">
        <Status status={job.last_status}/>
      </div>
      <div className="col-md-9 block">
        <span className="title">
          <i className="fa fa-tasks icon" aria-hidden="true"/>
          {job.unique_name}
        </span>
        <div className="meta">
          <span className="meta-info">
            <i className="fa fa-circle icon" aria-hidden="true"/>
            <span className="title">id:</span>
            {job.id}
          </span>
        </div>
        {job.resources &&
        <div className="meta meta-resources">
          {Object.keys(job.resources)
            .filter(
              (res, idx) =>
                job.resources[res] != null
            )
            .map(
            (res, idx) =>
              <span className="meta-info" key={idx}>
                <i className="fa fa-microchip icon" aria-hidden="true"/>
                <span className="title">{res}:</span>
                {job.resources[res].requests || ''} - {job.resources[res].limits || ''}
              </span>
          )}
        </div>
        }
      </div>
      <div className="col-md-2 block">
        <TaskRunMetaInfo startedAt={job.started_at} finishedAt={job.finished_at}/>
      </div>
    </div>
  );
}

export default Job;
