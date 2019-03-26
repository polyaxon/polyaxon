import * as _ from 'lodash';
import { connect } from 'react-redux';
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

interface OwnProps {
  user: string;
  projectName?: string;
  useFilters?: boolean;
  endpointList?: string;
  showBookmarks?: boolean;
  showDeleted?: boolean;
  fetchData?: () => search_actions.SearchAction;
  fetchSearches?: () => search_actions.SearchAction;
}

export function mapStateToProps(state: AppState, ownProps: OwnProps) {
  // let useFilter = () => {
  //   let groups: GroupModel[] = [];
  //   let project = state.projects.byUniqueNames[ownProps.projectName];
  //   let groupNames = project.groups;
  //   groupNames = getPaginatedSlice(groupNames);
  //   groupNames.forEach(
  //     function (group: string, idx: number) {
  //       groups.push(state.groups.byUniqueNames[group]);
  //     });
  //   return {groups: groups, count: project.num_experiment_groups};
  // };

  const useLastFetched = () => {
    const groupNames = state.groups.lastFetched.names;
    const count = state.groups.lastFetched.count;
    const groups: GroupModel[] = [];
    groupNames.forEach(
      (group: string, idx: number) => {
        groups.push(state.groups.byUniqueNames[group]);
      });
    return {groups, count};
  };
  const results = useLastFetched();

  const isLoading = isTrue(state.loadingIndicators.groups.global.fetch);
  return {
    isCurrentUser: state.auth.user === ownProps.user,
    groups: results.groups,
    count: results.count,
    useFilters: isTrue(ownProps.useFilters),
    showBookmarks: isTrue(ownProps.showBookmarks),
    showDeleted: isTrue(ownProps.showDeleted),
    endpointList: ownProps.endpointList,
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

export function mapDispatchToProps(dispatch: Dispatch<actions.GroupAction>, params: any): DispatchProps {
  return {
    onCreate: (group: GroupModel) => dispatch(actions.createGroup(
      params.match.params.user,
      params.match.params.projectName,
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
      if (params.projectName) {
        return dispatch(search_actions.fetchExperimentGroupSearches(params.projectName));
      } else {
        throw new Error('Groups container does not have project.');
      }
    },
    createSearch: (data: SearchModel) => {
      if (params.projectName) {
        return dispatch(search_actions.createExperimentGroupSearch(params.projectName, data));
      } else {
        throw new Error('Builds container does not have project.');
      }
    },
    deleteSearch: (searchId: number) => {
      if (params.projectName) {
        return dispatch(search_actions.deleteExperimentGroupSearch(params.projectName, searchId));
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
      if (_.isNil(params.projectName) && params.endpointList === BOOKMARKS) {
        return dispatch(actions.fetchBookmarkedGroups(params.user, filters));
      } else if (_.isNil(params.projectName) && params.endpointList === ARCHIVES) {
        return dispatch(actions.fetchArchivedGroups(params.user, filters));
      } else if (params.projectName) {
        return dispatch(actions.fetchGroups(params.projectName, filters));
      } else {
        throw new Error('Groups container expects either a project name or bookmarks or archives.');
      }
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Groups);
