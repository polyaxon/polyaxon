import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';

import { ActionInterface } from '../../interfaces/actions';

import '../actions.less';

export interface Props {
  onDelete: () => any;
  onStop: () => any;
  tensorboardActionCallback?: () => any;
  hasTensorboard?: boolean;
  isRunning: boolean;
  pullRight: boolean;
  actions?: ActionInterface[];
}

function ExperimentActions(props: Props) {
  const actions = props.actions || [];
  return (
    <span className={props.pullRight ? 'actions pull-right' : 'actions'}>
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
          {actions.map((action: ActionInterface, idx: number) => (
            <MenuItem key={idx} eventKey="1" onClick={action.callback}>
              <i className={`fa fa-${action.icon} icon`} aria-hidden="true"/> {action.name}
            </MenuItem>
          ))}
          {props.onStop && props.isRunning &&
          <MenuItem eventKey="1" onClick={props.onStop}>
            <i className="fa fa-stop icon" aria-hidden="true"/> Stop
          </MenuItem>
          }
          {props.tensorboardActionCallback && props.hasTensorboard &&
          <MenuItem eventKey="2" onClick={props.tensorboardActionCallback}>
            <i
              className="fa fa-stop icon"
              aria-hidden="true"
            /> Stop Tensorboard
          </MenuItem>
          }
          <MenuItem eventKey="2" onClick={props.onDelete}>
          <i className="fa fa-trash icon" aria-hidden="true"/> Delete
        </MenuItem>
        </Dropdown.Menu>
      </Dropdown>
    </span>
  );
}

export default ExperimentActions;
