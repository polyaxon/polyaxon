import * as moment from 'moment';
import * as React from 'react';

import { humanizeTimeDelta } from '../../utils/humanize';
import MetaInfo from './metaInfo';

export interface Props {
  startedAt: Date | string;
  finishedAt: Date | string;
  inline?: boolean;
}

function TaskRunMetaInfo({startedAt, finishedAt, inline = false}: Props) {
  let totalRun = humanizeTimeDelta(startedAt, finishedAt);
  let startedAtM = startedAt ? moment(startedAt) : null;
  let finishedAtM = finishedAt ? moment(finishedAt) : null;
  return (
    <span>
        {startedAtM &&
        <MetaInfo
          icon="far fa-clock"
          name="Started"
          tooltip={startedAtM.format('YYYY-MM-DD HH:mm:ss')}
          value={startedAtM.fromNow()}
          inline={inline}
        />
        }
      {finishedAtM &&
      <MetaInfo
        icon="far fa-clock"
        name="Finished"
        tooltip={finishedAtM.format('YYYY-MM-DD HH:mm:ss')}
        value={finishedAtM.fromNow()}
        inline={inline}
      />
      }
      {totalRun &&
      <MetaInfo
        icon="fas fa-hourglass"
        name="Total run"
        value={totalRun}
        inline={inline}
      />
      }
    </span>
  );
}

export default TaskRunMetaInfo;
