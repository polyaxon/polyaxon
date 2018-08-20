import * as React from 'react';

import './action.less';

export interface Props {
  onDelete: () => any;
  onStop?: () => any;
  isRunning: boolean;
}

function Actions({onDelete, onStop, isRunning = false}: Props) {
  return (
    <div className="btn-group action">
      <button
        type="button"
        className="btn btn-default dropdown-toggle"
        data-toggle="dropdown"
        aria-haspopup="true"
        aria-expanded="false"
      >
        More <span className="caret"/>
      </button>
      <ul className="dropdown-menu">
        {onStop && isRunning &&
          <li><a onClick={onStop}>Stop</a></li>
        }
        {onStop && isRunning &&
          <li role="separator" className="divider"/>
        }
        <li><a className="delete" onClick={onDelete}> Delete</a></li>
      </ul>
    </div>

  );
}

export default Actions;
