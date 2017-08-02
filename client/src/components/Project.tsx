import * as React from "react";
import {ProjectModel} from "../models/project";


function Project(props: ProjectModel) {
  return (
    <div className="project">
      Project { props.name }
    </div>
  );
}

export default Project;
