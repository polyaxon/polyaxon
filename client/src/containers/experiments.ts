import * as _ from 'lodash';
import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import Experiments from '../components/experiments';
import { AppState } from '../constants/types';
import { isTrue } from '../constants/utils';
import { ExperimentModel } from '../models/experiment';

import * as actions from '../actions/experiment';
import * as search_actions from '../actions/search';
import { getExperimentIndexName } from '../constants/utils';

interface OwnProps {
  user: string;
  projectName?: string;
  groupId?: string | number;
  useFilters?: boolean;
  bookmarks?: boolean;
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
    bookmarks: isTrue(ownProps.bookmarks),
  };
}

export interface DispatchProps {
  onCreate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onDelete: (experimentName: string) => actions.ExperimentAction;
  onStop: (experimentName: string) => actions.ExperimentAction;
  onUpdate: (experiment: ExperimentModel) => actions.ExperimentAction;
  fetchData?: (offset?: number, query?: string, sort?: string) => actions.ExperimentAction;
  fetchSearches?: () => search_actions.SearchAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentAction>, ownProps: OwnProps): DispatchProps {
  return {
    onCreate: (experiment: ExperimentModel) => dispatch(actions.createExperimentActionCreator(experiment)),
    onDelete: (experimentName: string) => dispatch(actions.deleteExperiment(experimentName)),
    onStop: (experimentName: string) => dispatch(actions.stopExperiment(experimentName)),
    onUpdate: (experiment: ExperimentModel) => dispatch(actions.updateExperimentActionCreator(experiment)),
    fetchSearches: () => {
      if (ownProps.projectName) {
        return dispatch(search_actions.fetchProjectExperimentSearches(ownProps.projectName));
      } else {
        throw new Error('Experiments container does not have project.');
      }
    },
    fetchData: (offset?: number,
                query?: string,
                sort?: string,
                extraFilters?:  {[key: string]: number|boolean|string}) => {
      const filters: {[key: string]: number|boolean|string} = {};
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
      if (_.isNil(ownProps.projectName) && ownProps.bookmarks) {
        return dispatch(actions.fetchBookmarkedExperiments(ownProps.user, filters));
      } else if (ownProps.projectName) {
        return dispatch(actions.fetchExperiments(ownProps.projectName, filters));
      } else {
        throw new Error('Experiments container expects either a project name or bookmarks.');
      }
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Experiments);
