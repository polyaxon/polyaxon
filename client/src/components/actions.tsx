import * as React from 'react';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';

export interface Props {
  onDelete: () => any;
  onStop?: () => any;
  isRunning: boolean;
}

function Actions({onDelete, onStop, isRunning = false}: Props) {
  return (
    <div className="btn-toolbar action" role="toolbar">
      {onStop && isRunning &&
        <OverlayTrigger placement="bottom" overlay={<Tooltip id="tooltipId">Stop</Tooltip>}>
          <button className="btn btn-default btn-sm" onClick={onStop}>
            <i className="fa fa-stop icon" aria-hidden="true"/>
          </button>
        </OverlayTrigger>
      }
      <OverlayTrigger placement="bottom" overlay={<Tooltip id="tooltipId">Delete</Tooltip>}>
      <button className="btn btn-default btn-sm" onClick={onDelete}>
        <i className="fa fa-trash icon" aria-hidden="true"/>
      </button>
      </OverlayTrigger>
    </div>

  );
}

export default Actions;
