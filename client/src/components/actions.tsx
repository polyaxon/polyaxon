import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';
import './actions.less';

export interface Props {
  onDelete: () => any;
  onStop?: () => any;
  isRunning: boolean;
  pullRight?: boolean;
}

function Actions({onDelete, onStop, isRunning = false, pullRight = false}: Props) {
  return (
    <span className={pullRight ? 'actions pull-right' : 'actions'}>
      <Dropdown
        pullRight={true}
        key={1}
        id={`dropdown-actions-1`}
      >
        <Dropdown.Toggle
          bsStyle="default"
          bsSize="small"
          noCaret={true}
        >
            <i className="fa fa-ellipsis-h icon" aria-hidden="true"/>
        </Dropdown.Toggle>
        <Dropdown.Menu>
        {onStop && isRunning &&
        <MenuItem eventKey="1" onClick={onStop}>
          <i className="fa fa-stop icon" aria-hidden="true"/> Stop
        </MenuItem>
        }
        <MenuItem eventKey="2" onClick={onDelete}>
          <i className="fa fa-trash icon" aria-hidden="true"/> Delete
        </MenuItem>
        </Dropdown.Menu>
      </Dropdown>
    </span>
  );
}

export default Actions;
