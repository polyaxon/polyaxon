import * as React from "react";
import * as _ from "lodash";

import Job from "./job";
import {JobModel} from "../models/job";


export interface Props {
  jobs: JobModel[];
  onCreate: (job: JobModel) => any;
  onUpdate: (job: JobModel) => any;
  onDelete: (job: JobModel) => any;
  fetchData: () => any
}


export default class Jobs extends React.Component<Props, Object> {
  componentDidMount() {
    const {jobs, onCreate, onUpdate, onDelete, fetchData} = this.props;
    fetchData();
  }

  public render() {
    const {jobs, onCreate, onUpdate, onDelete, fetchData} = this.props;
    return (
      <div className="row">
        <div className="col-md-12">
          <ul>
            {jobs.filter(
              (job: JobModel) => _.isNil(job.deleted) || !job.deleted
            ).map(
              (job: JobModel) =>
                <li className="list-item" key={job.uuid}>
                  <Job job={job} onDelete={() => onDelete(job)}/>
                </li>)}
          </ul>
        </div>
      </div>
    );
  }
}
