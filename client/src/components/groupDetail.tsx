import * as React from "react";
import * as _ from "lodash";

import {GroupModel} from "../models/group";
import Experiments from "../containers/experiments";


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
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <a className="back-button" onClick={() => {
              window.history.back()
            }}>&#060;</a>
            <span className="title">
              <i className="fa fa-object-group icon" aria-hidden="true"></i>
              Group: {group.unique_name}
            </span>
            <span className="results-info">({group.num_experiments} experiments found)</span>
            {group.content &&
            <pre className="content">
              {group.content}
            </pre>
            }
          </div>
          <Experiments fetchData={() => null} user={group.user} projectName={group.project_name}
                       groupUuid={group.uuid}></Experiments>
        </div>
      </div>
    );
  }
}
