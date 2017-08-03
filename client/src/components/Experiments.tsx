import * as React from "react";
import {ExperimentModel} from "../models/experiment";
import Experiment from "./Experiment";

export interface Props {
  experiments: ExperimentModel[];
  onCreate?: (experiment: ExperimentModel) => any;
  onUpdate?: (experiment: ExperimentModel) => any;
  onDelete?: (experimentId: number) => any;
}


function Experiments({experiments, onCreate, onUpdate, onDelete}: Props) {
  return (
    <ul>
      {experiments.map(xp => <li key={xp.id}><Experiment experiment={xp} onDelete={() => onDelete(xp.id)}/></li>)}
    </ul>
  );
}

export default Experiments;
