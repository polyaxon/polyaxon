import * as React from 'react';

import { BuildModel } from '../models/build';
import TaskRunMetaInfo from './taskRunMetaInfo';
import Status from './status';

export interface Props {
  build: BuildModel;
  onDelete: () => void;
}

function Build({build, onDelete}: Props) {
  let buildDetailUrl = `builds/${build.id}/`;

  return (
    <div className="row">
      <div className="col-md-1 block">
        <Status status={build.last_status}/>
      </div>
      <div className="col-md-9 block">
        <span className="title">
          <i className="fa fa-tasks icon" aria-hidden="true"/>
          {build.unique_name}
        </span>
        <div className="meta">
          <span className="meta-info">
            <i className="fa fa-circle icon" aria-hidden="true"/>
            <span className="title">id:</span>
            {build.id}
          </span>
        </div>
        {build.resources &&
        <div className="meta meta-resources">
          {Object.keys(build.resources)
            .filter(
              (res, idx) =>
                build.resources[res] != null
            )
            .map(
            (res, idx) =>
              <span className="meta-info" key={idx}>
                <i className="fa fa-microchip icon" aria-hidden="true"/>
                <span className="title">{res}:</span>
                {build.resources[res].requests || ''} - {build.resources[res].limits || ''}
              </span>
          )}
        </div>
        }
      </div>
      <div className="col-md-2 block">
        <TaskRunMetaInfo startedAt={build.started_at} finishedAt={build.finished_at}/>
      </div>
    </div>
  );
}

export default Build;
