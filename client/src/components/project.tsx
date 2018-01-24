import * as React from "react";
import {LinkContainer} from "react-router-bootstrap";
import * as moment from "moment";

import {pluralize} from "../constants/utils"
import {ProjectModel} from "../models/project";
import {getProjectUrl} from "../constants/utils";

export interface Props {
  project: ProjectModel;
  onDelete: () => void;
}

function Project({project, onDelete}: Props) {
  let visibility = project.is_public ? 'Public' : 'Private';
  return (
    <div className="row">
      <div className="col-md-10 block">
        <LinkContainer to={getProjectUrl(project.user, project.name)}>
          <a className="title">
            <i className="fa fa-server icon" aria-hidden="true"></i>
            {project.name}
          </a>
        </LinkContainer>
        <div className="meta-description">
          {project.description}
        </div>
        <div className="meta">
          <span className="meta-info">
            <i className="fa fa-lock icon" aria-hidden="true"></i>
            <span className="title">Visibility:</span>
            {visibility}
          </span>
          <span className="meta-info">
            <i className="fa fa-clock-o icon" aria-hidden="true"></i>
            <span className="title">Last updated:</span>
            {moment(project.updated_at).fromNow()}
          </span>
        </div>
      </div>

      <div className="col-md-2 block">
        <div className="row">
          <span>
            <i className="fa fa-cube icon" aria-hidden="true"></i>
          </span>
          <span>
            {project.num_experiments} {pluralize('Experiment', project.num_experiments)}
          </span>
        </div>
        <div className="row">
          <span>
            <i className="fa fa-cubes icon" aria-hidden="true"></i>
          </span>
          <span>
            {project.num_experiment_groups} {pluralize('Experiment Group', project.num_experiment_groups)}
          </span>
        </div>
      </div>
    </div>
  );
}

export default Project;
