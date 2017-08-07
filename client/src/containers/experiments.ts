import { connect, Dispatch } from "react-redux";

import { AppState } from "../types/index";
import Experiments from "../components/Experiments";
import {ExperimentModel} from "../models/experiment";
import * as actions from "../actions/experiment";


export function mapStateToProps(state: AppState)  {
  if (state.experiments)
    return {experiments: (<any>Object).values(state.experiments.byIds)};
  return [];
}

export interface DispatchProps {
  onCreate?: (experiment: ExperimentModel) => any;
  onDelete?: (experimentId: number) => any;
  onUpdate?: (experiment: ExperimentModel) => any;
  fetchData?: () => any;
}


export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentAction>): DispatchProps {
  return {
    onCreate: (experiment: ExperimentModel) => dispatch(actions.createExperiment(experiment)),
    onDelete: (experimentId: number) => dispatch(actions.deleteExperiment(experimentId)),
    onUpdate: (experiment: ExperimentModel) => dispatch(actions.updateExperiment(experiment)),
    fetchData: () => dispatch(actions.fetchExperiments())
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Experiments);
