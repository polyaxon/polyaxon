import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import Groups from '../../components/groups/groups';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { GroupModel } from '../../models/group';

import * as actions from '../../actions/groups';
import * as search_actions from '../../actions/search';
import { ACTIONS } from '../../constants/actions';
import { SearchModel } from '../../models/search';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { getErrorsGlobal } from '../../utils/errors';
import { getLastFetchedGroups } from '../../utils/states';

interface Props extends RouteComponentProps<any> {
  user?: string;
  projectName?: string;
  useFilters?: boolean;
  endpointList?: string;
  showBookmarks?: boolean;
  showDeleted?: boolean;
  fetchData?: () => search_actions.SearchAction;
  fetchSearches?: () => search_actions.SearchAction;
}

export function mapStateToProps(state: AppState, props: Props) {
  const cUser = props.user || props.match.params.user;
  const results = getLastFetchedGroups(state.groups);
  const isLoading = isTrue(state.loadingIndicators.groups.global.fetch);
  return {
    isCurrentUser: state.auth.user === cUser,
    groups: results.groups,
    count: results.count,
    useFilters: isTrue(props.useFilters),
    showBookmarks: isTrue(props.showBookmarks),
    showDeleted: isTrue(props.showDeleted),
    endpointList: props.endpointList,
    isLoading,
    errors: getErrorsGlobal(state.alerts.groups.global, isLoading, ACTIONS.FETCH),
  };
}

export interface DispatchProps {
  onCreate?: (group: GroupModel) => actions.GroupAction;
  onDelete: (groupName: string) => actions.GroupAction;
  onStop: (groupName: string) => actions.GroupAction;
  onArchive: (groupName: string) => actions.GroupAction;
  onRestore: (groupName: string) => actions.GroupAction;
  bookmark: (groupName: string) => actions.GroupAction;
  unbookmark: (groupName: string) => actions.GroupAction;
  onUpdate?: (group: GroupModel) => actions.GroupAction;
  fetchData?: (offset?: number, query?: string, sort?: string) => actions.GroupAction;
  fetchSearches?: () => search_actions.SearchAction;
  createSearch?: (data: SearchModel) => search_actions.SearchAction;
  deleteSearch?: (searchId: number) => search_actions.SearchAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.GroupAction>, props: Props): DispatchProps {
  const cUser = props.user || props.match.params.user;
  const cProjectName = props.projectName || `${cUser}.${props.match.params.projectName}`;

  return {
    onCreate: (group: GroupModel) => dispatch(actions.createGroup(
      props.match.params.user,
      props.match.params.projectName,
      group,
      true)),
    onDelete: (groupName: string) => dispatch(actions.deleteGroup(groupName)),
    onStop: (groupName: string) => dispatch(actions.stopGroup(groupName)),
    onArchive: (groupName: string) => dispatch(actions.archiveGroup(groupName)),
    onRestore: (groupName: string) => dispatch(actions.restoreGroup(groupName)),
    bookmark: (groupName: string) => dispatch(actions.bookmark(groupName)),
    unbookmark: (groupName: string) => dispatch(actions.unbookmark(groupName)),
    onUpdate: (group: GroupModel) => dispatch(actions.updateGroup(group.unique_name, group)),
    fetchSearches: () => {
      if (cProjectName) {
        return dispatch(search_actions.fetchExperimentGroupSearches(cProjectName));
      } else {
        throw new Error('Groups container does not have project.');
      }
    },
    createSearch: (data: SearchModel) => {
      if (cProjectName) {
        return dispatch(search_actions.createExperimentGroupSearch(cProjectName, data));
      } else {
        throw new Error('Builds container does not have project.');
      }
    },
    deleteSearch: (searchId: number) => {
      if (cProjectName) {
        return dispatch(search_actions.deleteExperimentGroupSearch(cProjectName, searchId));
      } else {
        throw new Error('Builds container does not have project.');
      }
    },
    fetchData: (offset?: number, query?: string, sort?: string) => {
      const filters: { [key: string]: number | boolean | string } = {};
      if (query) {
        filters.query = query;
      }
      if (sort) {
        filters.sort = sort;
      }
      if (offset) {
        filters.offset = offset;
      }
      if (props.endpointList === BOOKMARKS) {
        return dispatch(actions.fetchBookmarkedGroups(cUser, filters));
      } else if (props.endpointList === ARCHIVES) {
        return dispatch(actions.fetchArchivedGroups(cUser, filters));
      } else if (cProjectName) {
        return dispatch(actions.fetchGroups(cProjectName, filters));
      } else {
        throw new Error('Groups container expects either a project name or bookmarks or archives.');
      }
    }
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Groups));
