import * as React from 'react';
import * as _ from 'lodash';
import { LinkContainer } from 'react-router-bootstrap';

import {
  getBuildUrl,
  getExperimentUrl,
  getGroupUrl,
  splitUniqueName
} from '../constants/utils';

import { ExperimentModel } from '../models/experiment';
import Status from './status';
import Description from './description';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import UserMetaInfo from './metaInfo/userMetaInfo';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import LinkMetaInfo from './metaInfo/linkMetaInfo';

export interface Props {
  experiment: ExperimentModel;
  onDelete: () => void;
}

function Experiment({experiment, onDelete}: Props) {
  let values = splitUniqueName(experiment.project);
  let groupUrl = '';
  if (!_.isNil(experiment.experiment_group)) {
    let groupValues = splitUniqueName(experiment.experiment_group);
    groupUrl = getGroupUrl(groupValues[0], groupValues[1], groupValues[2]);
  }
  let buildValues = splitUniqueName(experiment.build_job);
  let buildUrl = getBuildUrl(buildValues[0], buildValues[1], buildValues[2]);
  return (
    <div className="row">
      <div className="col-md-1 block">
        <Status status={experiment.last_status}/>
      </div>
      <div className="col-md-7 block">
        <LinkContainer to={getExperimentUrl(values[0], values[1], experiment.id)}>
          <a className="title">
            <i className="fa fa-cube icon" aria-hidden="true"/>
            {experiment.unique_name}
          </a>
        </LinkContainer>
        <Description description={experiment.description}/>
        <div className="meta">
          <UserMetaInfo user={experiment.user} inline={true}/>
          <DatesMetaInfo
            createdAt={experiment.created_at}
            updatedAt={experiment.updated_at}
            inline={true}
          />
        </div>
      </div>
      <div className="col-md-2 block">
        {groupUrl &&
        <LinkMetaInfo
          icon="fa-asterisk"
          name="Group"
          value={groupUrl}
        />}
        <LinkMetaInfo
          icon="fa-asterisk"
          name="Build"
          value={buildUrl}
        />
      </div>
      <div className="col-md-2 block">
        <TaskRunMetaInfo startedAt={experiment.started_at} finishedAt={experiment.finished_at}/>
      </div>
    </div>
  );
}

export default Experiment;
