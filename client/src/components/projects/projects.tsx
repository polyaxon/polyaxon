import * as React from 'react';

import * as actions from '../../actions/project';
import { ProjectModel } from '../../models/project';
import { BOOKMARKS } from '../../utils/endpointList';
import { isLive } from '../../utils/isLive';
import { EmptyBookmarks } from '../empty/emptyBookmarks';
import { EmptyList } from '../empty/emptyList';
import PaginatedTable from '../tables/paginatedTable';
import Project from './project';
import ProjectHeader from './projectHeader';

export interface Props {
  isCurrentUser: boolean;
  user: string;
  projects: ProjectModel[];
  count: number;
  showBookmarks: boolean;
  showDeleted: boolean;
  endpointList: string;
  onUpdate: (project: ProjectModel) => actions.ProjectAction;
  onDelete: (projectName: string) => actions.ProjectAction;
  onArchive: (projectName: string) => actions.ProjectAction;
  onRestore: (projectName: string) => actions.ProjectAction;
  bookmark: (projectName: string) => actions.ProjectAction;
  unbookmark: (projectName: string) => actions.ProjectAction;
  fetchData: () => actions.ProjectAction;
}

export default class Projects extends React.Component<Props, {}> {
  public render() {
    const projects = this.props.projects;
    const listProjects = () => {
      return (
        <table className="table table-hover table-responsive">
          <tbody>
          {ProjectHeader()}
          {projects
            .filter(
              (projet: ProjectModel) =>
                (!this.props.showDeleted && isLive(projet)) || (this.props.showDeleted && !isLive(projet)))
            .map(
              (project: ProjectModel) =>
                <Project
                  key={project.unique_name}
                  project={project}
                  onDelete={() => this.props.onDelete(project.unique_name)}
                  onArchive={() => this.props.onArchive(project.unique_name)}
                  onRestore={() => this.props.onRestore(project.unique_name)}
                  showBookmarks={this.props.showBookmarks}
                  bookmark={() => this.props.bookmark(project.unique_name)}
                  unbookmark={() => this.props.unbookmark(project.unique_name)}
                />)}
          </tbody>
        </table>
      );
    };

    const empty = this.props.endpointList === BOOKMARKS ?
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
