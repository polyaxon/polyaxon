import * as React from "react";
import {ProjectModel} from "../models/project";
import Project from "./Project";
import {isNullOrUndefined} from "util";

export interface Props {
  projects: ProjectModel[];
  onCreate?: (project: ProjectModel) => any;
  onUpdate?: (project: ProjectModel) => any;
  onDelete?: (projectId: number) => any;
}


function Projects({projects, onCreate, onUpdate, onDelete}: Props) {
  return (
    <ul>
      {projects.map(project => <li key={project.id}><Project project={project} onDelete={() => onDelete(project.id)}/></li>)}
    </ul>
  );
}

export default Projects;
