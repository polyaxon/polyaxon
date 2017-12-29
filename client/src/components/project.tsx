import * as React from "react";
import {Button, ButtonToolbar} from "react-bootstrap";
import {LinkContainer} from "react-router-bootstrap";
import {dateOptions} from "../constants/utils"

import {ProjectModel} from "../models/project";


export interface Props {
  project: ProjectModel;
  onDelete: () => void;
}

function Project({project, onDelete}: Props) {
  return (
    <div className="row">
      <div className="col-md-12 project">
        <ButtonToolbar className="pull-right">
          <LinkContainer to={`/${project.user}/${project.name}/experiments`}><Button>View experiments</Button></LinkContainer>
        </ButtonToolbar>
        <h4 className="title"><a>{ project.name }</a></h4>
        <div className="meta"><b>Number of Experiments: </b>{ project.num_experiments }</div>
        <div className="meta"><b>Created at: </b>{ project.createdAt.toLocaleTimeString("en-US", dateOptions) }</div>
      </div>
    </div>
  );
}

export default Project;
