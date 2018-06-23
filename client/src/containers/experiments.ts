import { connect, Dispatch } from 'react-redux';

import { getGroupName } from '../constants/utils';
import { AppState } from '../constants/types';
import Experiments from '../components/experiments';
import { ExperimentModel } from '../models/experiment';

import * as actions from '../actions/experiment';
import { getPaginatedSlice } from '../constants/paginate';
import { getOffset } from '../constants/paginate';

interface OwnProps {
  user: string;
  projectName: string;
  groupId?: string;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, ownProps: any) {
  let groupName = ownProps.groupId != null ?
                  getGroupName(ownProps.projectName, ownProps.groupId) :
                  null;
  let experiments: ExperimentModel[] = [];
  let count = 0;
  if (groupName != null) {
    let group = state.groups.byUniqueNames[groupName];
    count = group.num_experiments;
    let experimentNames = group.experiments;
    experimentNames = getPaginatedSlice(experimentNames);
    experimentNames.forEach(
      function (experiment: string, idx: number) {
        experiments.push(state.experiments.byUniqueNames[experiment]);
      });
  } else {
    let project = state.projects.byUniqueNames[ownProps.projectName];
    count = project.num_independent_experiments;
    let experimentNames = project.experiments.filter(
      (experiment) => state.experiments.byUniqueNames[experiment].experiment_group == null
    );
    experimentNames = getPaginatedSlice(experimentNames);
    experimentNames.forEach(
      function (experiment: string, idx: number) {
        experiments.push(state.experiments.byUniqueNames[experiment]);
      });
  }

  return {isCurrentUser: state.auth.user === ownProps.user, experiments: experiments, count: count};
}

export interface DispatchProps {
  onCreate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onDelete?: (experiment: ExperimentModel) => actions.ExperimentAction;
  onUpdate?: (experiment: ExperimentModel) => actions.ExperimentAction;
  fetchData?: (currentPage?: number) => actions.ExperimentAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentAction>, ownProps: OwnProps): DispatchProps {
  return {
    onCreate: (experiment: ExperimentModel) => dispatch(actions.createExperimentActionCreator(experiment)),
    onDelete: (experiment: ExperimentModel) => dispatch(actions.deleteExperimentActionCreator(experiment)),
    onUpdate: (experiment: ExperimentModel) => dispatch(actions.updateExperimentActionCreator(experiment)),
    fetchData: (currentPage?: number) => {
      let filters: {[key: string]: number|boolean|string} = {};
      if (ownProps.groupId) {
        filters.group = ownProps.groupId;
      }
      if (!ownProps.groupId) {
        filters.independent = true;
      }
      let offset = getOffset(currentPage);
      if (offset != null) {
        filters.offset = offset;
      }
      return dispatch(actions.fetchExperiments(ownProps.projectName, filters));
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Experiments);
