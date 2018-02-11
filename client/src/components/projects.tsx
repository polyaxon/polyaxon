import * as React from 'react';
import * as _ from 'lodash';

import Project from './project';
import RootModal from '../containers/modal';
import { ProjectModel } from '../models/project';
import { pluralize } from '../constants/utils';
import PaginatedList from '../constants/components';

export interface Props {
  user: string;
  projects: ProjectModel[];
  count: number;
  onUpdate: (project: ProjectModel) => any;
  onDelete: (project: ProjectModel) => any;
  fetchData: () => any;
  showModal: () => any;
  hideModal: () => any;
}

export default class Projects extends React.Component<Props, Object> {
  public render() {
    const {user, projects, onUpdate, onDelete, fetchData, showModal, hideModal} = this.props;
    const listProjects = (
      <ul>
        {projects.filter(
          (project: ProjectModel) => _.isNil(project.deleted) || !project.deleted
        ).map(
          (project: ProjectModel) => <li className="list-item" key={project.unique_name}>
            <Project project={project} onDelete={() => onDelete(project)}/></li>)}
      </ul>
    );
    return (
      <div>
        <div className="entity-details">
          <span className="title">{user}</span>
          <span className="results-info">[{projects.length} {pluralize('Project', projects.length)}]</span>
        </div>
        <RootModal hideModal={hideModal}/>
        <PaginatedList
          count={this.props.count}
          componentList={listProjects}
          fetchData={this.props.fetchData}
        />
      </div>
    );
  }
}
