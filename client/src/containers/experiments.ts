import { connect, Dispatch } from "react-redux";
import * as _ from "lodash";

import { AppState } from "../constants/types";
import Experiments from "../components/experiments";
import {ExperimentModel} from "../models/experiment";
import * as actions from "../actions/experiment";

interface OwnProps {
  projectId?: number;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, ownProps: OwnProps) {
  let experimentIds: any = [];
  if (!_.isNil(ownProps.projectId) && !_.isEmpty(state.projects.byIds)){
    experimentIds = state.projects.byIds[ownProps.projectId].experiments
  }

  if (state.experiments) {
    if (_.isEmpty(experimentIds)) {
      return {experiments: (<any>Object).values(state.experiments.byIds)};
    } else {
      return {experiments: state.experiments.ids.filter(
        (k: number) => _.includes(experimentIds, k)).map((k: number) => state.experiments.byIds[k])};
    }
  }
  return [];
}

export interface DispatchProps {
  onCreate?: (experiment: ExperimentModel) => any;
  onDelete?: (experimentId: number) => any;
  onUpdate?: (experiment: ExperimentModel) => any;
  fetchData?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentAction>, ownProps: OwnProps): DispatchProps {
  return {
    onCreate: (experiment: ExperimentModel) => dispatch(actions.createExperiment(experiment)),
    onDelete: (experimentId: number) => dispatch(actions.deleteExperiment(experimentId)),
    onUpdate: (experiment: ExperimentModel) => dispatch(actions.updateExperiment(experiment)),
    fetchData: () => dispatch(ownProps.fetchData? ownProps.fetchData : actions.fetchExperiments())
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Experiments);
