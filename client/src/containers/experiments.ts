import * as _ from 'lodash';
import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as actions from '../actions/experiment';
import * as groupActions from '../actions/group';
import * as searchActions from '../actions/search';
import Experiments from '../components/experiments/experiments';
import { AppState } from '../constants/types';
import { getExperimentIndexName, isTrue } from '../constants/utils';
import { ExperimentModel } from '../models/experiment';
import { GroupModel } from '../models/group';
import { SearchModel } from '../models/search';
import { ARCHIVES, BOOKMARKS } from '../utils/endpointList';

interface OwnProps {
  user: string;
  projectName?: string;
  groupId?: number;
  useFilters?: boolean;
  showBookmarks?: boolean;
  showDeleted?: boolean;
  useCheckbox?: boolean;
  endpointList?: string;
  fetchData?: () => actions.ExperimentAction;
}

export function mapStateToProps(state: AppState, ownProps: OwnProps) {
  // let useFilter = () => {
  //   let groupName = ownProps.groupId != null ?
  //     getGroupName(ownProps.projectName, ownProps.groupId) :
  //     null;
  //   let experiments: ExperimentModel[] = [];
  //   let count = 0;
  //   if (groupName != null) {
  //     let group = state.groups.byUniqueNames[groupName];
  //     count = group.num_experiments;
  //     let experimentNames = group.experiments;
  //     experimentNames = getPaginatedSlice(experimentNames);
  //     experimentNames.forEach(
  //       function (experiment: string, idx: number) {
  //         experiments.push(state.experiments.byUniqueNames[experiment]);
  //       });
  //   } else {
  //     let project = state.projects.byUniqueNames[ownProps.projectName];
  //     count = project.num_independent_experiments;
  //     let experimentNames = project.experiments.filter(
  //       (experiment) => state.experiments.byUniqueNames[experiment].experiment_group == null
  //     );
  //     experimentNames = getPaginatedSlice(experimentNames);
  //     experimentNames.forEach(
  //       function (experiment: string, idx: number) {
  //         experiments.push(state.experiments.byUniqueNames[experiment]);
  //       });
  //   }
  //   return {experiments: experiments, count: count};
  // };

  const useLastFetched = () => {
    const experimentNames = state.experiments.lastFetched.names;
    const count = state.experiments.lastFetched.count;
    const experiments: ExperimentModel[] = [];
    experimentNames.forEach(
      (experiment: string, idx: number) => {
        experiments.push(state.experiments.byUniqueNames[getExperimentIndexName(experiment)]);
      });
    return {experiments, count};
  };
  const results = useLastFetched();

  return {
    isCurrentUser: state.auth.user === ownProps.user,
    experiments: results.experiments,
    groupId: ownProps.groupId,
    count: results.count,
    useFilters: isTrue(ownProps.useFilters),
    showBookmarks: isTrue(ownProps.showBookmarks),
    showDeleted: isTrue(ownProps.showDeleted),
    useCheckbox: isTrue(ownProps.useCheckbox),
    endpointList: ownProps.endpointList,
  };
}

export interface DispatchProps {
  onCreate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onDelete: (experimentName: string) => actions.ExperimentAction;
  onDeleteMany: (experimentIds: number[]) => actions.ExperimentAction;
  onStop: (experimentName: string) => actions.ExperimentAction;
  onArchive: (experimentName: string) => actions.ExperimentAction;
  onRestore: (experimentName: string) => actions.ExperimentAction;
  onStopMany: (experimentIds: number[]) => actions.ExperimentAction;
  bookmark: (experimentName: string) => actions.ExperimentAction;
  unbookmark: (experimentName: string) => actions.ExperimentAction;
  onUpdate: (experiment: ExperimentModel) => actions.ExperimentAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.ExperimentAction;
  fetchSearches: () => searchActions.SearchAction;
  createSearch: (data: SearchModel) => searchActions.SearchAction;
  deleteSearch: (searchId: number) => searchActions.SearchAction;
  createSelection: (data: GroupModel) => groupActions.GroupAction;
  addToSelection: (selectionId: number, items: number[]) => groupActions.GroupAction;
  removeFromSelection: (selectionId: number, items: number[]) => groupActions.GroupAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentAction>, ownProps: OwnProps): DispatchProps {
  return {
    onCreate: (experiment: ExperimentModel) => dispatch(actions.createExperimentActionCreator(experiment)),
    onDelete: (experimentName: string) => dispatch(actions.deleteExperiment(experimentName)),
    onDeleteMany: (experimentIds: number[]) => {
      if (ownProps.projectName) {
        return dispatch(actions.deleteExperiments(ownProps.projectName, experimentIds));
      } else {
        throw new Error('Experiments container does not have project.');
      }
    },
    onStop: (experimentName: string) => dispatch(actions.stopExperiment(experimentName)),
    onArchive: (experimentName: string) => dispatch(actions.archiveExperiment(experimentName)),
    onRestore: (experimentName: string) => dispatch(actions.restoreExperiment(experimentName)),
    onStopMany: (experimentIds: number[]) => {
      if (ownProps.projectName) {
        return dispatch(actions.stopExperiments(ownProps.projectName, experimentIds));
      } else {
        throw new Error('Experiments container does not have project.');
      }
    },
    bookmark: (experimentName: string) => dispatch(actions.bookmark(experimentName)),
    unbookmark: (experimentName: string) => dispatch(actions.unbookmark(experimentName)),
    onUpdate: (experiment: ExperimentModel) => dispatch(actions.updateExperimentActionCreator(experiment)),
    fetchSearches: () => {
      if (ownProps.projectName) {
        return dispatch(searchActions.fetchExperimentSearches(ownProps.projectName));
      } else {
        throw new Error('Experiments container does not have project.');
      }
    },
    createSearch: (data: SearchModel) => {
      if (ownProps.projectName) {
        return dispatch(searchActions.createExperimentSearch(ownProps.projectName, data));
      } else {
        throw new Error('Experiments container does not have project.');
      }
    },
    deleteSearch: (searchId: number) => {
      if (ownProps.projectName) {
        return dispatch(searchActions.deleteExperimentSearch(ownProps.projectName, searchId));
      } else {
        throw new Error('Experiments container does not have project.');
      }
    },
    createSelection: (data: GroupModel) => {
      if (ownProps.projectName) {
        return dispatch(groupActions.createGroup(ownProps.projectName, data));
      } else {
        throw new Error('Experiments container does not have project.');
      }
    },
    addToSelection: (selectionId: number, items: number[]) => {
      if (ownProps.projectName) {
        const data = {experiment_ids: items, operation: 'add'};
        const groupName = `${ownProps.projectName}.${selectionId}`;
        return dispatch(groupActions.updateSelection(groupName, data));
      } else {
        throw new Error('Experiments container does not have project.');
      }
    },
    removeFromSelection: (selectionId: number, items: number[]) => {
      if (ownProps.projectName) {
        const data = {experiment_ids: items, operation: 'remove'};
        const groupName = `${ownProps.projectName}.${selectionId}`;
        return dispatch(groupActions.updateSelection(groupName, data));
      } else {
        throw new Error('Experiments container does not have project.');
      }
    },
    fetchData: (offset?: number,
                query?: string,
                sort?: string,
                extraFilters?: { [key: string]: number | boolean | string }) => {
      const filters: { [key: string]: number | boolean | string } = {};
      if (ownProps.groupId) {
        filters.group = ownProps.groupId;
      }
      if (extraFilters && (extraFilters.metrics === true || extraFilters.metrics === 'true')) {
        filters.metrics = extraFilters.metrics;
      }
      if (extraFilters && (extraFilters.declarations === true || extraFilters.declarations === 'true')) {
        filters.declarations = extraFilters.declarations;
      }
      if (extraFilters && (extraFilters.independent === true || extraFilters.independent === 'true')) {
        filters.independent = extraFilters.independent;
      }
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
        return dispatch(actions.fetchBookmarkedExperiments(ownProps.user, filters));
      } else if (_.isNil(ownProps.projectName) && ownProps.endpointList === ARCHIVES) {
        return dispatch(actions.fetchArchivedExperiments(ownProps.user, filters));
      } else if (ownProps.projectName) {
        return dispatch(actions.fetchExperiments(ownProps.projectName, filters));
      } else {
        throw new Error('Experiments container expects either a project name or bookmarks or archives.');
      }
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Experiments);
