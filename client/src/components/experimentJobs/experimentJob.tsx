import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import { ExperimentJobModel } from '../../models/experimentJob';
import { getExperimentJobUrl, splitUniqueName } from '../../urls/utils';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import IdMetaInfo from '../metaInfo/idMetaInfo';
import NodeMetaInfo from '../metaInfo/nodeMetaInfo';
import PodIdMetaInfo from '../metaInfo/podIdMetaInfo';
import ResourcesMetaInfo from '../metaInfo/resourcesMetaInfo';
import TaskRunMetaInfo from '../metaInfo/taskRunMetaInfo';
import Status from '../statuses/status';

export interface Props {
  experimentJob: ExperimentJobModel;
}

function ExperimentJob({experimentJob}: Props) {
  const values = splitUniqueName(experimentJob.unique_name);
  return (
    <div className="row">
      <div className="col-md-1 block">
        <Status status={experimentJob.last_status}/>
      </div>
      <div className="col-md-7 block">
        <LinkContainer to={getExperimentJobUrl(values[0], values[1], experimentJob.experiment, experimentJob.id)}>
          <a className="title">
            <i className="fas fa-tasks icon" aria-hidden="true"/>
            {experimentJob.name || experimentJob.unique_name}
          </a>
        </LinkContainer>
        <div className="meta">
          <PodIdMetaInfo value={experimentJob.pod_id} inline={true}/>
        </div>
        <div className="meta">
          <NodeMetaInfo node={experimentJob.node_scheduled} inline={true}/>
        </div>
        <div className="meta">
          <DatesMetaInfo
            createdAt={experimentJob.created_at}
            updatedAt={experimentJob.updated_at}
            inline={true}
          />
        </div>
        <div className="meta">
          <ResourcesMetaInfo resources={experimentJob.resources}/>
        </div>
      </div>
      <div className="col-md-2 block">
        <div className="meta">
          <span className="meta-info">
            <i className="fas fa-certificate icon" aria-hidden="true"/>
            <span className="title">Role:</span>
            {experimentJob.role}
          </span>
        </div>
        <div className="meta">
          <IdMetaInfo value={experimentJob.id} inline={true}/>
        </div>
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
