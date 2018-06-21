import * as React from 'react';
import * as _ from 'lodash';

import Project from './project';
import RootModal from '../containers/modal';
import { ProjectModel } from '../models/project';
import PaginatedList from '../components/paginatedList';
import { EmptyList } from './emptyList';
import Breadcrumb from './breadcrumb';
import ProjectHeader from './projectHeader';

export interface Props {
  isCurrentUser: boolean;
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
        return (
          <ul>
            {projects.filter(
              (project: ProjectModel) => _.isNil(project.deleted) || !project.deleted
            ).map(
              (project: ProjectModel) => <li className="list-item" key={project.unique_name}>
                <Project project={project} onDelete={() => this.props.onDelete(project)}/></li>)}
          </ul>
        );
      }
    ;

    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <Breadcrumb links={[{name: this.props.user}, {name: 'projects'}]}/>
          </div>
          <RootModal hideModal={this.props.hideModal}/>
          <PaginatedList
            count={this.props.count}
            componentList={listProjects()}
            componentHeader={ProjectHeader()}
            componentEmpty={EmptyList(
              this.props.isCurrentUser,
              'project',
              'project',
              'polyaxon project create --help')}
            fetchData={this.props.fetchData}
          />
        </div>
      </div>
    );
  }
}
