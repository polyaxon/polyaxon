import * as React from 'react';
import * as moment from 'moment';

import { humanizeTimeDelta } from '../../constants/utils';
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
          icon="fa-clock-o"
          name="Started"
          tooltip={startedAtM.format('YYYY-MM-DD HH:mm:ss')}
          value={startedAtM.fromNow()}
          inline={inline}
        />
        }
      {finishedAtM &&
      <MetaInfo
        icon="fa-clock-o"
        name="Finished"
        tooltip={finishedAtM.format('YYYY-MM-DD HH:mm:ss')}
        value={finishedAtM.fromNow()}
        inline={inline}
      />
      }
      {totalRun &&
      <MetaInfo
        icon="fa-hourglass"
        name="Total run"
        value={totalRun}
        inline={inline}
      />
      }
    </span>
  );
}

export default TaskRunMetaInfo;
