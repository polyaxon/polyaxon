import * as React from 'react';
import * as _ from 'lodash';
import * as moment from 'moment';
import { LinkContainer } from 'react-router-bootstrap';

import { GroupModel } from '../models/group';
import Experiments from '../containers/experiments';
import {
  getCssClassForStatus,
  getProjectUrl,
  getUserUrl,
  splitProjectName
} from '../constants/utils';
import TaskRunMetaInfo from './taskRunMetaInfo';

export interface Props {
  group: GroupModel;
  onDelete: () => undefined;
  fetchData: () => undefined;
}

export default class GroupDetail extends React.Component<Props, Object> {
  componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const group = this.props.group;
    if (_.isNil(group)) {
      return (<div>Nothing</div>);
    }
    let statusCssClass = getCssClassForStatus(group.last_status);
    let values = splitProjectName(group.project_name);
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <span className="title">
              <i className="fa fa-cubes icon" aria-hidden="true"/>
              <LinkContainer to={getUserUrl(values[0])}>
                <span>
                  <a className="title">
                    {values[0]}
                  </a>/
                </span>
              </LinkContainer>
              <LinkContainer to={getProjectUrl(values[0], values[1])}>
                <span>
                  <a className="title">
                    {values[1]}
                  </a>/
                </span>
              </LinkContainer>
              <span className="title">
                Group {group.sequence}
              </span>
            </span>
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
              <span className="meta-info">
                <i className="fa fa-share-alt icon" aria-hidden="true"/>
                <span className="title">Concurrency:</span>
                {group.concurrency}
              </span>
              {group.current_iteration > 0 &&
              <span className="meta-info">
                <i className="fa fa-refresh icon" aria-hidden="true"/>
                <span className="title">Iteration:</span>
                {group.current_iteration}
              </span>
              }
              <TaskRunMetaInfo startedAt={group.started_at} finishedAt={group.finished_at} inline={true}/>
              <span className={`status alert alert-${statusCssClass}`}>{group.last_status}
              </span>
            </div>
            <div className="meta">
              <span className="meta-info">
                <i className="fa fa-asterisk icon" aria-hidden="true"/>
                <span className="title">Algorithm:</span>
                {group.search_algorithm}
              </span>
              <span className="meta-info">
                <i className="fa fa-cube icon" aria-hidden="true"/>
                <span className="title">Experiments:</span>
                {group.num_experiments}
              </span>
              <span className="meta-info">
                <i className="fa fa-hourglass-1 icon" aria-hidden="true"/>
                <span className="title">Scheduled:</span>
                {group.num_scheduled_experiments}
              </span>
              <span className="meta-info">
                <i className="fa fa-hourglass-end icon" aria-hidden="true"/>
                <span className="title">Pending:</span>
                {group.num_pending_experiments}
              </span>
              <span className="meta-info">
                <i className="fa fa-bolt icon" aria-hidden="true"/>
                <span className="title">Running:</span>
                {group.num_running_experiments}
              </span>
              <span className="meta-info">
                <i className="fa fa-check icon" aria-hidden="true"/>
                <span className="title">Succeeded:</span>
                {group.num_succeeded_experiments}
              </span>
              <span className="meta-info">
                <i className="fa fa-close icon" aria-hidden="true"/>
                <span className="title">Failed:</span>
                {group.num_failed_experiments}
              </span>
              <span className="meta-info">
                <i className="fa fa-stop icon" aria-hidden="true"/>
                <span className="title">Stopped:</span>
                {group.num_stopped_experiments}
              </span>
            </div>
          </div>
          <h4 className="polyaxon-header">Experiments</h4>
          <Experiments user={group.user} projectName={group.project_name} groupSequence={group.sequence}/>
        </div>
      </div>
    );
  }
}
