import * as React from "react";
import * as _ from "lodash";
import {Button} from "react-bootstrap";

import Project from "./project";
import RootModal from "../containers/modal"
import {ProjectModel} from "../models/project";

export interface Props {
  projects: ProjectModel[];
  onUpdate: (project: ProjectModel) => any;
  onDelete: (project: ProjectModel) => any;
  fetchData: () => any;
  showModal: () => any;
  hideModal: () => any;
}


export default class Projects extends React.Component<Props, Object> {
  componentDidMount() {
    const {projects, onUpdate, onDelete, fetchData, showModal, hideModal} = this.props;
    fetchData();
  }

  public render() {
    const {projects, onUpdate, onDelete, fetchData, showModal, hideModal} = this.props;
    return (
      <div>
        <div className="entity-details">
          <span className="title">Projects</span>
          <span className="results-info">({projects.length} found)</span>
        </div>
        <RootModal hideModal={hideModal} />
        <ul>
          {projects.filter(
            (project: ProjectModel) => _.isNil(project.deleted) || !project.deleted
          ).map(
            (project: ProjectModel) => <li className="list-item" key={project.uuid}><Project project={project} onDelete={() => onDelete(project)}/></li>)}
        </ul>
      </div>
    );
  }
}
