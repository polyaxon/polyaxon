import * as React from "react";

import {Button, ButtonToolbar} from "react-bootstrap";
import {LinkContainer} from "react-router-bootstrap";
import {dateOptions, urlifyProjectName, getCssClassForStatus} from "../constants/utils"

import {GroupModel} from "../models/group";


export interface Props {
  group: GroupModel;
  onDelete: () => void;
}


function Group({group, onDelete}: Props) {
  let disabled = group.num_experiments == 0 ? true : false;
  return (
    <div className="row">
      <div className="col-md-12 block">
        <ButtonToolbar className="pull-right">
          <LinkContainer to={ `groups/${group.sequence}/` }>
            <Button className="button" disabled={disabled}>
              { group.num_experiments } Experiment{ group.num_experiments != 1 && 's' }
              <i className="fa fa-sliders icon" aria-hidden="true"></i>
            </Button>
          </LinkContainer>
        </ButtonToolbar>
        <span className="title">
          <i className="fa fa-object-group icon" aria-hidden="true"></i>
          Group: { group.unique_name}
        </span>
        <div className="meta">
          <i className="fa fa-user-o icon" aria-hidden="true"></i>
          <span className="title">User:</span>
          { group.user }
        </div>
        <div className="meta">
          <i className="fa fa-bolt icon" aria-hidden="true"></i>
          <span className="title">Concurrency:</span>
          { group.concurrency }
        </div>
        <div className="meta">
          <i className="fa fa-sliders icon" aria-hidden="true"></i>
          <span className="title">Number of pending experiments:</span>
          { group.num_pending_experiments }
        </div>
        <div className="meta">
          <i className="fa fa-sliders icon" aria-hidden="true"></i>
          <span className="title">Number of running experiments:</span>
          { group.num_running_experiments }
        </div>
        <div className="meta">
          <i className="fa fa-clock-o icon" aria-hidden="true"></i>
          <span className="title">Created at:</span>
          { group.createdAt.toLocaleTimeString("en-US", dateOptions) }
        </div>
      </div>
    </div>
  );
}

export default Group;
