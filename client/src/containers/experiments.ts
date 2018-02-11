import { connect, Dispatch } from 'react-redux';

import { getGroupName, sortByUpdatedAt } from '../constants/utils';
import { AppState } from '../constants/types';
import Experiments from '../components/experiments';
import { ExperimentModel } from '../models/experiment';

import * as actions from '../actions/experiment';

interface OwnProps {
  user: string;
  projectName: string;
  groupSequence?: string;
  count: number;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, ownProps: any) {
  let groupName = ownProps.groupSequence != null ?
                  getGroupName(ownProps.projectName, ownProps.groupSequence) :
                  null;
  let experiments: ExperimentModel[] = [];
  if (groupName != null) {
    state.groups.byUniqueNames[groupName].experiments.forEach(
      function (experiment: string, idx: number) {
        experiments.push(state.experiments.byUniqueNames[experiment]);
      });
  } else {
    state.projects.byUniqueNames[ownProps.projectName].experiments.filter(
      (experiment) => state.experiments.byUniqueNames[experiment].experiment_group_name == null
    ).forEach(
      function (experiment: string, idx: number) {
        experiments.push(state.experiments.byUniqueNames[experiment]);
      });
  }

  return {experiments: experiments.sort(sortByUpdatedAt), count: ownProps.count};
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
    fetchData: (currentPage?: number) => dispatch(
      actions.fetchExperiments(ownProps.projectName, currentPage, ownProps.groupSequence))
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Experiments);
