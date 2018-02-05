import * as React from 'react';
import * as moment from 'moment';

import { JobModel } from '../models/job';
import { getCssClassForStatus, humanizeTimeDelta } from '../constants/utils';

export interface Props {
  job: JobModel;
  onDelete: () => void;
}

function Job({job, onDelete}: Props) {
  let totalRun = humanizeTimeDelta(job.started_at, job.finished_at);
  let statusCssClass = getCssClassForStatus(job.last_status);
  let jobDetailUrl = `jobs/${job.sequence}/`;

  return (
    <div className="row">
      <div className="col-md-10 block">
        <span className="title">
          <i className="fa fa-tasks icon" aria-hidden="true"/>
          {job.unique_name}
          <span className={`status alert alert-${statusCssClass}`}>{job.last_status}</span>
        </span>
        <div className="meta">
          <span className="meta-info">
            <i className="fa fa-certificate icon" aria-hidden="true"/>
            <span className="title">Role:</span>
            {job.role}
          </span>
          <span className="meta-info">
            <i className="fa fa-circle icon" aria-hidden="true"/>
            <span className="title">Sequence:</span>
            {job.sequence}
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
        {job.started_at &&
        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-clock-o icon" aria-hidden="true"/>
            <span className="title">Started:</span>
            {moment(job.started_at).fromNow()}
          </span>
        </div>
        }
        {job.finished_at &&
        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-clock-o icon" aria-hidden="true"/>
            <span className="title">Finished:</span>
            {moment(job.finished_at).fromNow()}
          </span>
        </div>
        }
        {totalRun &&
        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-hourglass icon" aria-hidden="true"/>
            <span className="title">Total run:</span>
            {totalRun}
          </span>
        </div>
        }
      </div>
    </div>
  );
}

export default Job;
