import * as React from "react";

import Project from "./Project";
import {ProjectModel} from "../models/project";

export interface Props {
  projects: ProjectModel[];
  onCreate?: (project: ProjectModel) => any;
  onUpdate?: (project: ProjectModel) => any;
  onDelete?: (projectId: number) => any;
  fetchData: () => any
}


export default class Projects extends React.Component<Props, Object> {
  componentDidMount() {
    const {projects, onCreate, onUpdate, onDelete, fetchData} = this.props;
    fetchData();
  }

  public render() {
    const {projects, onCreate, onUpdate, onDelete, fetchData} = this.props;
    return (
      <ul>
        {projects.map(project => <li key={project.id}><Project project={project} onDelete={() => onDelete(project.id)}/></li>)}
      </ul>
    );
  }
}
