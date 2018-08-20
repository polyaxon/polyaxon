import * as _ from 'lodash';
import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as actions from '../actions/group';
import Groups from '../components/groups';
import { AppState } from '../constants/types';
import { isTrue } from '../constants/utils';
import { GroupModel } from '../models/group';

interface OwnProps {
  user: string;
  projectName?: string;
  useFilters?: boolean;
  bookmarks?: boolean;
  fetchData?: () => any;
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
    bookmarks: isTrue(ownProps.bookmarks),
  };
}

export interface DispatchProps {
  onCreate?: (group: GroupModel) => actions.GroupAction;
  onDelete?: (group: GroupModel) => actions.GroupAction;
  onUpdate?: (group: GroupModel) => actions.GroupAction;
  fetchData?: (offset?: number, query?: string, sort?: string) => actions.GroupAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.GroupAction>, ownProps: OwnProps): DispatchProps {
  return {
    onCreate: (group: GroupModel) => dispatch(actions.createGroupActionCreator(group)),
    onDelete: (group: GroupModel) => dispatch(actions.deleteGroupActionCreator(group)),
    onUpdate: (group: GroupModel) => dispatch(actions.updateGroupActionCreator(group)),
    fetchData: (offset?: number, query?: string, sort?: string) => {
      const filters: {[key: string]: number|boolean|string} = {};
      if (query) {
        filters.query = query;
      }
      if (sort) {
        filters.sort = sort;
      }
      if (offset) {
        filters.offset = offset;
      }
      if (_.isNil(ownProps.projectName) && ownProps.bookmarks) {
        return dispatch(actions.fetchBookmarkedGroups(ownProps.user, filters));
      } else if (ownProps.projectName) {
        return dispatch(actions.fetchGroups(ownProps.projectName, filters));
      } else {
        throw new Error('Groups container expects either a project name or bookmarks.');
      }
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Groups);
