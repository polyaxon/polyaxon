import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';

export interface Props {
  title: string;
  onClick: (item: string) => any;
  possibleValues: string[];
  selectedValues: string[];
}

function AutocompleteDropdown({title, onClick, possibleValues, selectedValues}: Props) {
  return (
    <Dropdown id={`dropdown-actions-1`}>
      <Dropdown.Toggle
        bsStyle="default"
        bsSize="small"
        noCaret={true}
      >
        <i className="fa fa-plus icon" aria-hidden="true"/> {title}
      </Dropdown.Toggle>
      <Dropdown.Menu>
        {possibleValues
          .filter((item: string) => selectedValues.indexOf(item) === -1)
          .map((item: string, idx: number) =>
          <MenuItem key={idx} eventKey="2" onClick={() => onClick(item)}>
            {item}
          </MenuItem>)
        }
      </Dropdown.Menu>
    </Dropdown>
  );
}

export default AutocompleteDropdown;
