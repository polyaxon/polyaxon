import * as React from "react";
import * as _ from "lodash";
import * as moment from "moment";
import {LinkContainer} from "react-router-bootstrap";

import {GroupModel} from "../models/group";
import Experiments from "../containers/experiments";
import {getProjectUrl, getUserUrl, splitProjectName} from "../constants/utils";


export interface Props {
  group: GroupModel;
  onDelete: () => any;
  fetchData: () => any;
}


export default class GroupDetail extends React.Component<Props, Object> {
  componentDidMount() {
    const {group, onDelete, fetchData} = this.props;
    fetchData();
  }

  public render() {
    const {group, onDelete, fetchData} = this.props;
    if (_.isNil(group)) {
      return (<div>Nothing</div>);
    }
    let values = splitProjectName(group.project_name);
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <span className="title">
              <i className="fa fa-cubes icon" aria-hidden="true"></i>
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
                <i className="fa fa-user-o icon" aria-hidden="true"></i>
                <span className="title">User:</span>
                {group.user}
              </span>
              <span className="meta-info">
                <i className="fa fa-clock-o icon" aria-hidden="true"></i>
                <span className="title">Last updated:</span>
                {moment(group.updated_at).fromNow()}
              </span>
              <span className="meta-info">
                <i className="fa fa-cube icon" aria-hidden="true"></i>
                <span className="title">Experiments:</span>
                {group.num_experiments}
              </span>
              <span className="meta-info">
                <i className="fa fa-share-alt icon" aria-hidden="true"></i>
                <span className="title">Concurrency:</span>
                {group.concurrency}
              </span>
              <span className="meta-info">
                <i className="fa fa-bolt icon" aria-hidden="true"></i>
                <span className="title">Running Experiments:</span>
                {group.num_running_experiments}
              </span>
              <span className="meta-info">
                <i className="fa fa-hourglass-end icon" aria-hidden="true"></i>
                <span className="title">Pending Experiments:</span>
                {group.num_pending_experiments}
              </span>
            </div>
          </div>
          <h4 className="polyaxon-header">Experiments</h4>
          <Experiments fetchData={() => null} user={group.user} projectName={group.project_name}
                       groupSequence={group.sequence}></Experiments>
        </div>
      </div>
    );
  }
}
