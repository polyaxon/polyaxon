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
  return (
    <span>
        {startedAt &&
        <MetaInfo
          icon="fa-clock-o"
          name="Started"
          tooltip={startedAt.toString()}
          value={moment(startedAt).fromNow()}
          inline={inline}
        />
        }
      {finishedAt &&
      <MetaInfo
        icon="fa-clock-o"
        name="Finished"
        tooltip={finishedAt.toString()}
        value={moment(finishedAt).fromNow()}
        inline={inline}
      />
      }
      {totalRun &&
      <MetaInfo
        icon="fa-hourglass"
        name="Total run"
        tooltip={totalRun}
        value={totalRun}
        inline={inline}
      />
      }
    </span>
  );
}

export default TaskRunMetaInfo;
