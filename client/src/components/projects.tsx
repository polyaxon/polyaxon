import * as React from 'react';

import * as actions from '../actions/project';
import PaginatedTable from '../components/paginatedTable';
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
        <tbody>
        {ProjectHeader()}
        {projects.map(
          (project: ProjectModel) =>
            <Project
              key={project.unique_name}
              project={project}
              onDelete={() => this.props.onDelete(project.unique_name)}
            />)}
        </tbody>
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
      <PaginatedTable
        count={this.props.count}
        componentList={listProjects()}
        componentEmpty={empty}
        filters={false}
        fetchData={this.props.fetchData}
      />
    );
  }
}
