import * as React from 'react';
import { DropdownButton, MenuItem } from 'react-bootstrap';

export interface Props {
  onDelete: () => any;
  onStop?: () => any;
  isRunning: boolean;
  pullRight?: boolean;
}

function Actions({onDelete, onStop, isRunning = false, pullRight = false}: Props) {
  return (
    <span className={pullRight ? 'pull-right' : ''}>
      <DropdownButton
        bsStyle="default"
        bsSize="small"
        pullRight={true}
        title=""
        key={1}
        id={`dropdown-basic-1`}
      >
        {onStop && isRunning &&
        <MenuItem eventKey="1" onClick={onStop}><i className="fa fa-stop icon" aria-hidden="true"/> Stop</MenuItem>
        }
        <MenuItem eventKey="2" onClick={onDelete}><i className="fa fa-trash icon" aria-hidden="true"/> Delete</MenuItem>
      </DropdownButton>
    </span>
  );
}

export default Actions;
