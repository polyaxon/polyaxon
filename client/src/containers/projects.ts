import { connect } from 'react-redux';
import { Dispatch } from 'redux';
import * as _ from 'lodash';

import { AppState } from '../constants/types';
import Projects from '../components/projects';
import { ProjectModel } from '../models/project';
import * as actions from '../actions/project';
import * as modalActions from '../actions/modal';

interface OwnProps {
  user: string;
  bookmarks?: boolean;
  fetchData?: () => any;
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

  let useLastFetched = () => {
    let projectNames = state.projects.lastFetched.names;
    let count = state.projects.lastFetched.count;
    let projects: ProjectModel[] = [];
    projectNames.forEach(
      function (project: string, idx: number) {
        projects.push(state.projects.byUniqueNames[project]);
      });
    return {projects: projects, count: count};
  };
  let results = useLastFetched();

  return {
    isCurrentUser: state.auth.user === ownProps.user,
    user: ownProps.user,
    projects: results.projects,
    count: results.count,
    bookmarks: !_.isNil(ownProps.bookmarks) && ownProps.bookmarks,
  };
}

export interface DispatchProps {
  onDelete?: (project: ProjectModel) => actions.ProjectAction;
  onUpdate?: (project: ProjectModel) => actions.ProjectAction;
  fetchData?: () => actions.ProjectAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<actions.ProjectAction | modalActions.ModalAction>, ownProps: OwnProps): DispatchProps {
  return {
    onDelete: (project: ProjectModel) => dispatch(actions.deleteProject(project)),
    onUpdate: (project: ProjectModel) => dispatch(actions.updateProjectActionCreator(project)),
    fetchData: (offset?: number) => {
      let filters: { [key: string]: number | boolean | string } = {};
      if (offset) {
        filters.offset = offset;
      }
      if (!_.isNil(ownProps.bookmarks) && ownProps.bookmarks) {
        return dispatch(actions.fetchBookmarkedProjects(ownProps.user, filters));
      } else if (ownProps.user) {
        return dispatch(actions.fetchProjects(ownProps.user, filters));
      } else {
        throw new Error('Projects container expects either a project name or bookmarks.');
      }
    },
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Projects);
