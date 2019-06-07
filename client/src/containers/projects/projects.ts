import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as actions from '../../actions/projects';
import Projects from '../../components/projects/projects';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { ProjectModel } from '../../models/project';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { getErrorsGlobal } from '../../utils/errors';
import { getLastFetchedProjects } from '../../utils/states';

interface Props {
  user: string;
  endpointList?: string;
  showBookmarks?: boolean;
  showDeleted?: boolean;
  fetchData?: () => actions.ProjectAction;
}

export function mapStateToProps(state: AppState, props: Props) {
  const results = getLastFetchedProjects(state.projects);

  const isLoading = isTrue(state.loadingIndicators.projects.global.fetch);
  return {
    isCurrentUser: state.auth.user === props.user,
    user: props.user,
    projects: results.projects,
    count: results.count,
    showBookmarks: isTrue(props.showBookmarks),
    showDeleted: isTrue(props.showDeleted),
    endpointList: props.endpointList,
    isLoading,
    errors: getErrorsGlobal(state.alerts.projects.global, isLoading, ACTIONS.FETCH),
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
  dispatch: Dispatch<actions.ProjectAction>, props: Props): DispatchProps {
  return {
    onDelete: (projectName: string) => dispatch(actions.deleteProject(projectName)),
    onArchive: (projectName: string) => dispatch(actions.archiveProject(projectName)),
    onRestore: (projectName: string) => dispatch(actions.restoreProject(projectName)),
    bookmark: (projectName: string) => dispatch(actions.bookmark(projectName)),
    unbookmark: (projectName: string) => dispatch(actions.unbookmark(projectName)),
    onUpdate: (project: ProjectModel) => dispatch(actions.updateProjectSuccessActionCreator(project)),
    fetchData: (offset?: number) => {
      const filters: { [key: string]: number | boolean | string } = {};
      if (offset) {
        filters.offset = offset;
      }
      if (props.endpointList === BOOKMARKS) {
        return dispatch(actions.fetchBookmarkedProjects(props.user, filters));
      } else if (props.endpointList === ARCHIVES) {
        return dispatch(actions.fetchArchivedProjects(props.user, filters));
      } else if (props.user) {
        return dispatch(actions.fetchProjects(props.user, filters));
      } else {
        throw new Error('Projects container expects either a project name or bookmarks or archives.');
      }
    },
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Projects);
