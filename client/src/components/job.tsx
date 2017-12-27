import * as React from "react";
import {Button, ButtonToolbar} from "react-bootstrap";
import {LinkContainer} from "react-router-bootstrap";

import {JobModel} from "../models/job";
import {dateOptions} from "../constants/utils"


export interface Props {
  job: JobModel;
  onDelete: () => void;
}


function Job({job, onDelete}: Props) {
  
  return (
    <div className="row">
      <div className="col-md-12 experiment">
        <h4 className="title"><a>{ job.unique_name}</a></h4>
        <div className="meta"><b>Uuid: </b> { job.uuid }</div>
        <div className="meta"><b>Sequence:</b> { job.sequence }</div>
        <div className="meta"><b>Role:</b> { job.role }</div>
        <div className="meta"><b>Experiment:</b> { job.experiment_name }</div>
        <div className="meta"><b>Last status:</b> { job.last_status }</div>
        <div className="meta"><b>Created at:</b> { job.createdAt.toLocaleTimeString("en-US", dateOptions) }</div>
      </div>
    </div>
  );
}

export default Job;
