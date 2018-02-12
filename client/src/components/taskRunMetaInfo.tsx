import * as React from 'react';
import * as moment from 'moment';

import { humanizeTimeDelta } from '../constants/utils';

export interface Props {
  startedAt: Date | string;
  finishedAt: Date | string;
  inline?: boolean;
}

function TaskRunMetaInfo({startedAt, finishedAt, inline = false}: Props) {
  let totalRun = humanizeTimeDelta(startedAt, finishedAt);
  if (inline) {
    return (
      <span>
      {startedAt &&
        <span className="meta-info">
            <i className="fa fa-clock-o icon" aria-hidden="true"/>
            <span className="title">Started:</span>
        {moment(startedAt).fromNow()}
        </span>
      }
        {finishedAt &&
          <span className="meta-info">
            <i className="fa fa-clock-o icon" aria-hidden="true"/>
            <span className="title">Finished:</span>
          {moment(finishedAt).fromNow()}
          </span>
        }
        {totalRun &&
          <span className="meta-info">
            <i className="fa fa-hourglass icon" aria-hidden="true"/>
            <span className="title">Total run:</span>
          {totalRun}
          </span>
        }
    </span>
    );
  } else {
    return (
      <span>
      {startedAt &&
      <div className="row meta">
        <span className="meta-info">
            <i className="fa fa-clock-o icon" aria-hidden="true"/>
            <span className="title">Started:</span>
          {moment(startedAt).fromNow()}
        </span>
      </div>
      }
        {finishedAt &&
        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-clock-o icon" aria-hidden="true"/>
            <span className="title">Finished:</span>
            {moment(finishedAt).fromNow()}
          </span>
        </div>
        }
        {totalRun &&
        <div className="row meta">
          <span className="meta-info">
            <i className="fa fa-hourglass icon" aria-hidden="true"/>
            <span className="title">Total run:</span>
            {totalRun}
          </span>
        </div>
        }
    </span>
    );
  }
}

export default TaskRunMetaInfo;
