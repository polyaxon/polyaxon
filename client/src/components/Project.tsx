import * as React from "react";
import {Button} from "react-bootstrap";

import {ProjectModel} from "../models/project";


export interface Props {
  project: ProjectModel;
  onDelete?: () => void;
}

function Project({project, onDelete}: Props) {
  return (
    <div className="project">
      Project { project.name }
      <Button className="warning" onClick={onDelete}>delete</Button>
    </div>
  );
}

export default Project;
