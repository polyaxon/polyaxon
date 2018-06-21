import * as React from 'react';

import { ExperimentJobModel } from '../models/experimentJob';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import Status from './status';

export interface Props {
  experimentJob: ExperimentJobModel;
  onDelete: () => void;
}

function ExperimentJob({experimentJob, onDelete}: Props) {
  let jobDetailUrl = `jobs/${experimentJob.id}/`;

  return (
    <div className="row">
      <div className="col-md-1 block">
        <Status status={experimentJob.last_status}/>
      </div>
      <div className="col-md-9 block">
        <span className="title">
          <i className="fa fa-tasks icon" aria-hidden="true"/>
          {experimentJob.unique_name}
        </span>
        <div className="meta">
          <span className="meta-info">
            <i className="fa fa-certificate icon" aria-hidden="true"/>
            <span className="title">Role:</span>
            {experimentJob.role}
          </span>
          <span className="meta-info">
            <i className="fa fa-circle icon" aria-hidden="true"/>
            <span className="title">id:</span>
            {experimentJob.id}
          </span>
        </div>
        {experimentJob.resources &&
        <div className="meta meta-resources">
          {Object.keys(experimentJob.resources)
            .filter(
              (res, idx) =>
                experimentJob.resources[res] != null
            )
            .map(
            (res, idx) =>
              <span className="meta-info" key={idx}>
                <i className="fa fa-microchip icon" aria-hidden="true"/>
                <span className="title">{res}:</span>
                {experimentJob.resources[res].requests || ''} - {experimentJob.resources[res].limits || ''}
              </span>
          )}
        </div>
        }
      </div>
      <div className="col-md-2 block">
        <TaskRunMetaInfo
          startedAt={experimentJob.started_at}
          finishedAt={experimentJob.finished_at}
        />
      </div>
    </div>
  );
}

export default ExperimentJob;
