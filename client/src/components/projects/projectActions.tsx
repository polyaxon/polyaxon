import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';

import '../actions.less';

export interface Props {
  onDelete: () => any;
  notebookActionCallback?: () => any;
  tensorboardActionCallback?: () => any;
  hasNotebook?: boolean;
  hasTensorboard?: boolean;
  pullRight: boolean;
}

function ProjectActions(props: Props) {
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
          {props.notebookActionCallback && props.hasTensorboard &&
          <MenuItem eventKey="2" onClick={props.notebookActionCallback}>
            <i
              className="fa fa-stop icon"
              aria-hidden="true"
            /> 'Stop Notebook'
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

export default ProjectActions;
