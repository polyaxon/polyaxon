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
      </div>
    </div>
  );
}

export default Job;
