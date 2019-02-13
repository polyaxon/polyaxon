import * as _ from 'lodash';
import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import Groups from '../components/groups/groups';
import { AppState } from '../constants/types';
import { isTrue } from '../constants/utils';
import { GroupModel } from '../models/group';

import * as actions from '../actions/group';
import * as search_actions from '../actions/search';
import { SearchModel } from '../models/search';
import { ARCHIVES, BOOKMARKS } from '../utils/endpointList';

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

  return {
    isCurrentUser: state.auth.user === ownProps.user,
    groups: results.groups,
    count: results.count,
    useFilters: isTrue(ownProps.useFilters),
    showBookmarks: isTrue(ownProps.showBookmarks),
    showDeleted: isTrue(ownProps.showDeleted),
    endpointList: ownProps.endpointList,
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

export function mapDispatchToProps(dispatch: Dispatch<actions.GroupAction>, ownProps: OwnProps): DispatchProps {
  return {
    onCreate: (group: GroupModel) => dispatch(actions.createGroupActionCreator(group)),
    onDelete: (groupName: string) => dispatch(actions.deleteGroup(groupName)),
    onStop: (groupName: string) => dispatch(actions.stopGroup(groupName)),
    onArchive: (groupName: string) => dispatch(actions.archiveGroup(groupName)),
    onRestore: (groupName: string) => dispatch(actions.restoreGroup(groupName)),
    bookmark: (groupName: string) => dispatch(actions.bookmark(groupName)),
    unbookmark: (groupName: string) => dispatch(actions.unbookmark(groupName)),
    onUpdate: (group: GroupModel) => dispatch(actions.updateGroupActionCreator(group)),
    fetchSearches: () => {
      if (ownProps.projectName) {
        return dispatch(search_actions.fetchExperimentGroupSearches(ownProps.projectName));
      } else {
        throw new Error('Groups container does not have project.');
      }
    },
    createSearch: (data: SearchModel) => {
      if (ownProps.projectName) {
        return dispatch(search_actions.createExperimentGroupSearch(ownProps.projectName, data));
      } else {
        throw new Error('Builds container does not have project.');
      }
    },
    deleteSearch: (searchId: number) => {
      if (ownProps.projectName) {
        return dispatch(search_actions.deleteExperimentGroupSearch(ownProps.projectName, searchId));
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
      if (_.isNil(ownProps.projectName) && ownProps.endpointList === BOOKMARKS) {
        return dispatch(actions.fetchBookmarkedGroups(ownProps.user, filters));
      } else if (_.isNil(ownProps.projectName) && ownProps.endpointList === ARCHIVES) {
        return dispatch(actions.fetchArchivedGroups(ownProps.user, filters));
      } else if (ownProps.projectName) {
        return dispatch(actions.fetchGroups(ownProps.projectName, filters));
      } else {
        throw new Error('Groups container expects either a project name or bookmarks or archives.');
      }
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Groups);
