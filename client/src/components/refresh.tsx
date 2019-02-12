import * as React from 'react';

export interface Props {
  pullRight: boolean;
  callback: () => any;
}

function Refresh({callback, pullRight}: Props) {
  const refresh = (
    <span className="pull-right">
      <button
        className="btn btn-sm btn-default"
        onClick={callback}
      >
        <i className="fa fa-refresh icon" aria-hidden="true"/> Refresh
      </button>
    </span>
  );

  if (pullRight) {
    return (
    <div className="pull-right button-refresh">
      {refresh}
    </div>
    );
  }
  return refresh;
}

export default Refresh;
