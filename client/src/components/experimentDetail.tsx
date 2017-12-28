import * as React from "react";
import * as _ from "lodash";
import {Button, ButtonToolbar} from "react-bootstrap";

import {ExperimentModel} from "../models/experiment";
import Jobs from "../containers/jobs";


export interface Props {
  experiment: ExperimentModel;
  onDelete: () => any;
  fetchData: () => any;
}


export default class ExperimentDetail extends React.Component<Props, Object> {
  componentDidMount() {
    const {experiment, onDelete, fetchData} = this.props;
    fetchData();
  }

  public render() {
    const {experiment, onDelete, fetchData} = this.props;
    if (_.isNil(experiment)) {
      return (<div>Nothing</div>);
    }
    return (
      <div className="row">
        <div className="col-md-12 project">
          <h3>
            <Button bsStyle="primary" onClick={() => {window.history.back()}}>Back</Button>
            &nbsp;{experiment.unique_name}: Jobs ({experiment.num_jobs} found)
          </h3>
          <Jobs fetchData={() => null} user={experiment.user} experiment={experiment}></Jobs>
        </div>
      </div>
    );
  }
}