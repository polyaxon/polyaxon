import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import { ActivityLogModel } from '../models/activitylog';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import {
  getUserUrl,
  getBuildUrl,
  getExperimentUrl,
  getGroupUrl,
  getJobUrl,
  splitUniqueName,
  urlifyProjectName,
} from '../constants/utils';

export interface Props {
  activityLog: ActivityLogModel;
}

function ActivityLog({activityLog}: Props) {
  const userUrl = getUserUrl(activityLog.actor);
  let objectUrl = '';
  if (activityLog.object_name) {
    if (activityLog.event_subject === 'project') {
      objectUrl = urlifyProjectName(activityLog.object_name);
    } else if (activityLog.event_subject === 'experiment') {
      let values = splitUniqueName(activityLog.object_name);
      let experimentId = (values.length === 4) ? values[3] : values[2];
      objectUrl = getExperimentUrl(values[0], values[1], experimentId);
    } else if (activityLog.event_subject === 'experiment_group') {
      let values = splitUniqueName(activityLog.object_name);
      objectUrl = getGroupUrl(values[0], values[1], values[2]);
    } else if (activityLog.event_subject === 'job') {
      let values = splitUniqueName(activityLog.object_name);
      objectUrl = getJobUrl(values[0], values[1], values[2]);
    } else if (activityLog.event_subject === 'job') {
      let values = splitUniqueName(activityLog.object_name);
      objectUrl = getBuildUrl(values[0], values[1], values[2]);
    } else if (activityLog.event_subject === 'user') {
      objectUrl = urlifyProjectName(activityLog.object_name);
    }
  }
  const activity = (
    <span>
      <LinkContainer to={userUrl}>
        <a>{activityLog.actor}</a>
      </LinkContainer> {activityLog.event_action} {activityLog.event_subject}:
      {' '}
      {objectUrl &&
      <LinkContainer to={objectUrl}><a>{activityLog.object_name}</a></LinkContainer>}
      {!objectUrl && <span>{activityLog.object_id}</span>}
    </span>
  );
  return (
    <div className="row">
      <div className="col-md-2 block">
        <div className="meta">
          <DatesMetaInfo createdAt={activityLog.created_at} inline={true}/>
        </div>
      </div>
      <div className="col-md-9 block">
        {activity}
      </div>
    </div>
  );
}

export default ActivityLog;
