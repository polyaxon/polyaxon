import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import { getExperimentJobUrl, splitUniqueName } from '../../constants/utils';
import { ExperimentJobModel } from '../../models/experimentJob';
import IdMetaInfo from '../metaInfo/idMetaInfo';
import NodeMetaInfo from '../metaInfo/nodeMetaInfo';
import PodIdMetaInfo from '../metaInfo/podIdMetaInfo';
import ResourcesMetaInfo from '../metaInfo/resourcesMetaInfo';
import TaskRunMetaInfo from '../metaInfo/taskRunMetaInfo';
import Status from '../status';

export interface Props {
  experimentJob: ExperimentJobModel;
  onDelete: () => void;
}

function ExperimentJob({experimentJob, onDelete}: Props) {
  const values = splitUniqueName(experimentJob.unique_name);
  return (
    <div className="row">
      <div className="col-md-1 block">
        <Status status={experimentJob.last_status}/>
      </div>
      <div className="col-md-7 block">
        <LinkContainer to={getExperimentJobUrl(values[0], values[1], experimentJob.experiment, experimentJob.id)}>
          <a className="title">
            <i className="fa fa-tasks icon" aria-hidden="true"/>
            {experimentJob.name || experimentJob.unique_name}
          </a>
        </LinkContainer>
        <div className="meta">
          <PodIdMetaInfo value={experimentJob.pod_id} inline={true}/>
        </div>
        <div className="meta">
          <span className="meta-info">
            <i className="fa fa-certificate icon" aria-hidden="true"/>
            <span className="title">Role:</span>
            {experimentJob.role}
          </span>
          <IdMetaInfo value={experimentJob.id} inline={true}/>
        </div>
        <ResourcesMetaInfo resources={experimentJob.resources}/>
      </div>
      <div className="col-md-2 block">
        <NodeMetaInfo node={experimentJob.node_scheduled}/>
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
