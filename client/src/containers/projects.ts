import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as modalActions from '../actions/modal';
import * as actions from '../actions/project';
import Projects from '../components/projects/projects';
import { AppState } from '../constants/types';
import { isTrue } from '../constants/utils';
import { ProjectModel } from '../models/project';
import { ARCHIVES, BOOKMARKS } from '../utils/endpointList';

interface OwnProps {
  user: string;
  endpointList?: string;
  showBookmarks?: boolean;
  showDeleted?: boolean;
  fetchData?: () => actions.ProjectAction;
}

export function mapStateToProps(state: AppState, ownProps: OwnProps) {
  // let useFilter = () => {
  //   let projects: ProjectModel[] = [];
  //   let user = state.users.byUserNames[username];
  //   if (user == null) {
  //     return {user: username, projects: <ProjectModel[]> [], count: 0};
  //   }
  //   let projectNames = user.projects;
  //   projectNames = getPaginatedSlice(projectNames);
  //   projectNames.forEach(
  //     function (project: string, idx: number) {
  //       projects.push(state.projects.byUniqueNames[project]);
  //     });
  //   return {projects: projects, count: user.num_projects};
  // };

  const useLastFetched = () => {
    const projectNames = state.projects.lastFetched.names;
    const count = state.projects.lastFetched.count;
    const projects: ProjectModel[] = [];
    projectNames.forEach(
      (project: string, idx: number) => {
        projects.push(state.projects.byUniqueNames[project]);
      });
    return {projects, count};
  };
  const results = useLastFetched();

  return {
    isCurrentUser: state.auth.user === ownProps.user,
    user: ownProps.user,
    projects: results.projects,
    count: results.count,
    showBookmarks: isTrue(ownProps.showBookmarks),
    showDeleted: isTrue(ownProps.showDeleted),
    endpointList: ownProps.endpointList,
  };
}

export interface DispatchProps {
  onDelete: (projectName: string) => actions.ProjectAction;
  onArchive: (projectName: string) => actions.ProjectAction;
  onRestore: (projectName: string) => actions.ProjectAction;
  bookmark: (projectName: string) => actions.ProjectAction;
  unbookmark: (projectName: string) => actions.ProjectAction;
  onUpdate?: (project: ProjectModel) => actions.ProjectAction;
  fetchData?: () => actions.ProjectAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<actions.ProjectAction | modalActions.ModalAction>, ownProps: OwnProps): DispatchProps {
  return {
    onDelete: (projectName: string) => dispatch(actions.deleteProject(projectName)),
    onArchive: (projectName: string) => dispatch(actions.archiveProject(projectName)),
    onRestore: (projectName: string) => dispatch(actions.restoreProject(projectName)),
    bookmark: (projectName: string) => dispatch(actions.bookmark(projectName)),
    unbookmark: (projectName: string) => dispatch(actions.unbookmark(projectName)),
    onUpdate: (project: ProjectModel) => dispatch(actions.updateProjectActionCreator(project)),
    fetchData: (offset?: number) => {
      const filters: { [key: string]: number | boolean | string } = {};
      if (offset) {
        filters.offset = offset;
      }
      if (ownProps.endpointList === BOOKMARKS) {
        return dispatch(actions.fetchBookmarkedProjects(ownProps.user, filters));
      } else if (ownProps.endpointList === ARCHIVES) {
        return dispatch(actions.fetchArchivedProjects(ownProps.user, filters));
      } else if (ownProps.user) {
        return dispatch(actions.fetchProjects(ownProps.user, filters));
      } else {
        throw new Error('Projects container expects either a project name or bookmarks or archives.');
      }
    },
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Projects);
