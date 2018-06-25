import * as React from 'react';
import * as _ from 'lodash';

import { JobModel } from '../models/job';
import Status from './status';
import Description from './description';
import UserMetaInfo from './metaInfo/userMetaInfo';
import TaskRunMetaInfo from './metaInfo/taskRunMetaInfo';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import Tags from './tags';

export interface Props {
  job: JobModel;
}

export default class JobOverview extends React.Component<Props, Object> {
  public render() {
    const job = this.props.job;

    if (_.isNil(job)) {
      return (<div>Nothing</div>);
    }
    return (
      <div className="entity-details">
        <div className="row">
          <div className="col-md-12">
             <Description
                description={job.description}
                showEmpty={true}
             />
            <div className="meta">
              <UserMetaInfo user={job.user} inline={true}/>
              <DatesMetaInfo
                createdAt={job.created_at}
                updatedAt={job.updated_at}
                inline={true}
              />
            </div>
            <div className="meta">
              <TaskRunMetaInfo startedAt={job.started_at} finishedAt={job.finished_at} inline={true}/>
              <Status status={job.last_status}/>
            </div>
            {job.resources &&
            <div className="meta meta-resources">
              {Object.keys(job.resources)
                .filter(
                  (res, idx) =>
                    job.resources[res] != null
                )
                .map(
                  (res, idx) =>
                    <span className="meta-info" key={idx}>
                <i className="fa fa-microchip icon" aria-hidden="true"/>
                <span className="title">{res}:</span>
                      {job.resources[res].requests || ''} - {job.resources[res].limits || ''}
              </span>
                )}
            </div>
            }
            <Tags tags={job.tags}/>
          </div>
        </div>
      </div>
    );
  }
}
