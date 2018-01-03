import * as React from "react";
import {Button, ButtonToolbar} from "react-bootstrap";
import {LinkContainer} from "react-router-bootstrap";
import {dateOptions, pluralize} from "../constants/utils"

import {ProjectModel} from "../models/project";


export interface Props {
  project: ProjectModel;
  onDelete: () => void;
}

function Project({project, onDelete}: Props) {
  let visibility = project.is_public ? 'Public' : 'Private';
  return (
    <div className="row">
      <div className="col-md-12 block">
        <ButtonToolbar className="pull-right">
          <LinkContainer to={`/${project.user}/${project.name}/`}>
            <Button className="button">
              {project.num_experiments} { pluralize('Experiment', project.num_experiments) }
              <i className="fa fa-sliders icon" aria-hidden="true"></i>
            </Button>
          </LinkContainer>
        </ButtonToolbar>
        <span className="title">
          <i className="fa fa-cubes icon" aria-hidden="true"></i>
          { project.name }
        </span>
        <div className="meta">
          <i className="fa fa-lock icon" aria-hidden="true"></i>
          <span className="title">Visibility:</span>
          { visibility }
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
