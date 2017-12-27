import * as React from "react";
import * as _ from "lodash";
import {Button, ButtonToolbar} from "react-bootstrap";
import {LinkContainer} from "react-router-bootstrap";

import Job from "./job";
import {ExperimentModel} from "../models/experiment";
import {JobModel} from "../models/job";
import {ProjectModel} from "../models/project";


export interface Props {
  experiment: ExperimentModel;
  jobs: JobModel[];
  onCreate: (job: JobModel) => any;
  onUpdate: (job: JobModel) => any;
  onDelete: (jobUuid: string) => any;
  fetchExperimentsData: () => any
  fetchJobsData: () => any
}


export default class Jobs extends React.Component<Props, Object> {
  componentDidMount() {
    const {jobs, experiment, onCreate, onUpdate, onDelete, fetchExperimentsData, fetchJobsData} = this.props;
    fetchExperimentsData();
    fetchJobsData();
  }

  public render() {
    const {jobs, experiment, onCreate, onUpdate, onDelete, fetchExperimentsData, fetchJobsData} = this.props;
    return (
        <div className="row">
          <div className="col-md-12">
            <h3>
              <Button bsStyle="primary" onClick={() => {window.history.back()}}>Back</Button>
              &nbsp;{experiment.unique_name}: Jobs ({jobs.length} found)
            </h3>
            <ul>
              {jobs.filter(
                (job: JobModel) => _.isNil(job.deleted) || !job.deleted
              ).map(
                (job: JobModel) => <li className="list-item" key={job.uuid}><Job job={job} onDelete={() => onDelete(job.uuid)}/></li>)}
            </ul>
          </div>
        </div>
    );
  }
}
