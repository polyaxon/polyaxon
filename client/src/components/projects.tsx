import * as React from 'react';
import * as _ from 'lodash';

import Project from './project';
import RootModal from '../containers/modal';
import { ProjectModel } from '../models/project';
import { pluralize } from '../constants/utils';
import PaginatedList from '../components/paginatedList';

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
    const projects = this.props.projects;
    const listProjects = () => {
      if (projects.length === 0) {
        return (
          <div className="row">
            <div className="col-md-offset-2 col-md-8">
              <div className="jumbotron jumbotron-action text-center">
                <h3>You don't have any project</h3>
                <img src="/static/images/project.svg" alt="project" className="empty-icon"/>
                <div>
                  You can create new project by using CLI: <b>polyaxon project create --help</b>
                </div>
              </div>
            </div>
          </div>
        );
      }
      return (
        <ul>
          {projects.filter(
            (project: ProjectModel) => _.isNil(project.deleted) || !project.deleted
          ).map(
            (project: ProjectModel) => <li className="list-item" key={project.unique_name}>
              <Project project={project} onDelete={() => this.props.onDelete(project)}/></li>)}
        </ul>
      );
    };

    return (
      <div>
        <div className="entity-details">
          <span className="title">{this.props.user}</span>
          <span className="results-info">[{projects.length} {pluralize('Project', projects.length)}]</span>
        </div>
        <RootModal hideModal={this.props.hideModal}/>
        <PaginatedList
          count={this.props.count}
          componentList={listProjects()}
          fetchData={this.props.fetchData}
        />
      </div>
    );
  }
}
