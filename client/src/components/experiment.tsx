import * as _ from 'lodash';
import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import {
  getBuildUrl,
  getExperimentUrl,
  getGroupUrl,
  splitUniqueName
} from '../constants/utils';

import { isDone } from '../constants/statuses';
import { ExperimentModel } from '../models/experiment';
import Actions from './actions';
import Description from './description';
import BuildLinkMetaInfo from './metaInfo/buildLinkMetaInfo';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import GroupLinkMetaInfo from './metaInfo/groupLinkMetaInfo';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import UserMetaInfo from './metaInfo/userMetaInfo';
import Status from './status';
import Tags from './tags';

export interface Props {
  experiment: ExperimentModel;
  onDelete: () => any;
  onStop: () => any;
}

function Experiment({experiment, onDelete, onStop}: Props) {
  const values = splitUniqueName(experiment.project);
  let groupUrl = '';
  let groupValues: string[] = [];
  if (!_.isNil(experiment.experiment_group)) {
    groupValues = splitUniqueName(experiment.experiment_group);
    groupUrl = getGroupUrl(groupValues[0], groupValues[1], groupValues[2]);
  }
  let buildUrl = '';
  let buildValues: string[] = [];
  if (!_.isNil(experiment.build_job)) {
    buildValues = splitUniqueName(experiment.build_job);
    buildUrl = getBuildUrl(buildValues[0], buildValues[1], buildValues[3]);
  }
  return (
    <div className="row">
      <div className="col-md-1 block">
        <Status status={experiment.last_status}/>
      </div>
      <div className="col-md-6 block">
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
        <Tags tags={experiment.tags}/>
      </div>
      <div className="col-md-2 block">
        <GroupLinkMetaInfo
          value={groupValues[2]}
          link={groupUrl}
        />
        <BuildLinkMetaInfo
          value={buildValues[3]}
          link={buildUrl}
        />
      </div>
      <div className="col-md-2 block">
        <TaskRunMetaInfo startedAt={experiment.started_at} finishedAt={experiment.finished_at}/>
      </div>
      <div className="col-md-1 block">
        <Actions
          onDelete={onDelete}
          onStop={onStop}
          isRunning={!isDone(experiment.last_status)}
        />
      </div>
    </div>
  );
}

export default Experiment;
