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
      <div className="col-md-12 block">
        <ButtonToolbar className="pull-right">
          <LinkContainer to={`/${project.user}/${project.name}/`}>
            <Button className="button">
              { project.num_experiments } Experiment{ project.num_experiments != 1 && 's' }
              <i className="fa fa-sliders icon" aria-hidden="true"></i>
            </Button>
          </LinkContainer>
        </ButtonToolbar>
        <span className="title">
          <i className="fa fa-cubes icon" aria-hidden="true"></i>
          { project.name }
        </span>
        <div className="meta">
          <i className="fa fa-sliders icon" aria-hidden="true"></i>
          <span className="title">Number of Experiments:</span>
          { project.num_experiments }
        </div>
        <div className="meta">
          <i className="fa fa-clock-o icon" aria-hidden="true"></i>
          <span className="title">Created at:</span>
          { project.createdAt.toLocaleTimeString("en-US", dateOptions) }
        </div>
      </div>
    </div>
  );
}

export default Project;
