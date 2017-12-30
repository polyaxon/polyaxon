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
        <div className="col-md-12">
          <div className="entity-details">
            <a className="back-button" onClick={() => {window.history.back()}}>&#060;</a>
            <span className="title">
              <i className="fa fa-sliders icon" aria-hidden="true"></i>
              {experiment.unique_name}
            </span>
            <span className="results-info">({experiment.num_jobs} jobs found)</span>
            <span className="experiment-content">
              {experiment.content}
            </span>
          </div>
          <Jobs fetchData={() => null} user={experiment.user} experiment={experiment}></Jobs>
        </div>
      </div>
    );
  }
}