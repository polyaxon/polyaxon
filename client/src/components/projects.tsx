import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../actions/project';
import PaginatedList from '../components/paginatedList';
import { ProjectModel } from '../models/project';
import { EmptyBookmarks } from './empty/emptyBookmarks';
import { EmptyList } from './empty/emptyList';
import Project from './project';
import ProjectHeader from './projectHeader';

export interface Props {
  isCurrentUser: boolean;
  user: string;
  projects: ProjectModel[];
  count: number;
  bookmarks: boolean;
  onUpdate: (project: ProjectModel) => actions.ProjectAction;
  onDelete: (projectName: string) => actions.ProjectAction;
  fetchData: () => actions.ProjectAction;
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
                <Project
                  project={project}
                  onDelete={() => this.props.onDelete(project.unique_name)}
                /></li>)}
          </ul>
        );
      };

    const empty = this.props.bookmarks ?
      EmptyBookmarks(
        this.props.isCurrentUser,
        'project',
        'project')
      : EmptyList(
        this.props.isCurrentUser,
        'project',
        'project',
        'polyaxon project create --help');

    return (
      <PaginatedList
        count={this.props.count}
        componentList={listProjects()}
        componentHeader={ProjectHeader()}
        componentEmpty={empty}
        filters={false}
        fetchData={this.props.fetchData}
      />
    );
  }
}
