import * as React from "react";
import {Button, ButtonToolbar} from "react-bootstrap";
import {LinkContainer} from "react-router-bootstrap";

import {JobModel} from "../models/job";
import {getCssClassForStatus} from "../constants/utils"


export interface Props {
  job: JobModel;
  onDelete: () => void;
}


function Job({job, onDelete}: Props) {
  let statusCssClass = getCssClassForStatus(job.last_status);
  let jobDetailUrl = `jobs/${job.sequence}/`;

  return (
    <div className="row">
      <div className="col-md-12 block">
        <ButtonToolbar className="pull-right">
          <LinkContainer to={ jobDetailUrl }>
            <Button className="button">
              Details
              <i className="fa fa-list-alt icon" aria-hidden="true"></i>
            </Button>
          </LinkContainer>
        </ButtonToolbar>
        <span className="title">
          <i className="fa fa-cube icon" aria-hidden="true"></i>
          { job.unique_name}
          <span className={`status alert alert-${statusCssClass}`}>{ job.last_status}</span>
        </span>
        { job.started_at &&
        <div className="meta">
          <i className="fa fa-clock-o icon" aria-hidden="true"></i>
          <span className="title">Started at:</span>
          { job.started_at }
        </div>
        }
        { job.finished_at &&
        <div className="meta">
          <i className="fa fa-clock-o icon" aria-hidden="true"></i>
          <span className="title">Finished at:</span>
          { job.finished_at }
        </div>
        }
      </div>
    </div>
  );
}

export default Job;
