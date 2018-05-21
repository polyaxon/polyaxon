import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';
import * as moment from 'moment';

import {
  getCssClassForStatus,
  getGroupUrl,
  splitProjectName
} from '../constants/utils';
import { GroupModel } from '../models/group';

export interface Props {
  group: GroupModel;
  onDelete: () => void;
}

function Group({group, onDelete}: Props) {
  let statusCssClass = getCssClassForStatus(group.last_status);
  let values = splitProjectName(group.project_name);
  return (
    <div className="row">
      <div className="col-md-10 block">
        <LinkContainer to={getGroupUrl(values[0], values[1], group.sequence)}>
          <a className="title">
            <i className="fa fa-cubes icon" aria-hidden="true"/>
            {group.unique_name}
            <span className={`status alert alert-${statusCssClass}`}>{group.last_status}</span>
          </a>
        </LinkContainer>
        <div className="meta-description">
          {group.description}
        </div>
        <div className="meta">
          <span className="meta-info">
            <i className="fa fa-user-o icon" aria-hidden="true"/>
            <span className="title">User:</span>
            {group.user}
          </span>
          <span className="meta-info">
            <i className="fa fa-clock-o icon" aria-hidden="true"/>
            <span className="title">Last updated:</span>
            {moment(group.updated_at).fromNow()}
          </span>
        </div>
      </div>

      <div className="col-md-2 block">
        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-asterisk icon" aria-hidden="true"/>
            <span className="title">Algorithm:</span>
            {group.search_algorithm}
          </span>
        </div>
        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-cube icon" aria-hidden="true"/>
            <span className="title">Experiments:</span>
            {group.num_experiments}
          </span>
        </div>

        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-share-alt icon" aria-hidden="true"/>
            <span className="title">Concurrency:</span>
            {group.concurrency}
          </span>
        </div>

        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-bolt icon" aria-hidden="true"/>
            <span className="title">Running Experiments:</span>
            {group.num_running_experiments}
          </span>
        </div>

        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-hourglass-end icon" aria-hidden="true"/>
            <span className="title">Pending Experiments:</span>
            {group.num_pending_experiments}
          </span>
        </div>
      </div>
    </div>
  );
}

export default Group;
