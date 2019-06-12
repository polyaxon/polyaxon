import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

import { getProjectUrl } from '../../urls/utils';

import '../actions.less';

export interface Props {
  user: string;
  projectName: string;
}

export default class ProjectAdd extends React.Component<Props, {}> {

  public render() {
    const projectUrl = getProjectUrl(this.props.user, this.props.projectName);
    return (
      <span className="actions actions-add pull-right">
      <Dropdown
        pullRight={true}
        key={1}
        id={`dropdown-actions-1`}
      >
        <Dropdown.Toggle
          bsStyle="success"
          bsSize="small"
          noCaret={true}
        >
            <i className="fas fa-plus fa-sm icon" aria-hidden="true"/> New
        </Dropdown.Toggle>
        <Dropdown.Menu>
          <LinkContainer to={`${projectUrl}/experiments/new`}>
            <MenuItem eventKey="2">
              <i
                className="fas fa-plus fa-sm icon"
                aria-hidden="true"
              /> Create experiment
            </MenuItem>
          </LinkContainer>
          <LinkContainer to={`${projectUrl}/groups/new`}>
            <MenuItem eventKey="3">
              <i
                className="fas fa-plus fa-sm icon"
                aria-hidden="true"
              /> Create experiment group
            </MenuItem>
          </LinkContainer>
          <LinkContainer to={`${projectUrl}/jobs/new`}>
            <MenuItem eventKey="6">
              <i
                className="fas fa-plus fa-sm icon"
                aria-hidden="true"
              /> Create job
            </MenuItem>
          </LinkContainer>
          <LinkContainer to={`${projectUrl}/builds/new`}>
            <MenuItem eventKey="7">
              <i
                className="fas fa-plus fa-sm icon"
                aria-hidden="true"
              /> Create build
            </MenuItem>
          </LinkContainer>
          <LinkContainer to={`${projectUrl}/notebooks/new`}>
            <MenuItem eventKey="4">
              <i
                className="fas fa-play fa-sm icon"
                aria-hidden="true"
              /> Start Notebook
            </MenuItem>
          </LinkContainer>
          <LinkContainer to={`${projectUrl}/tensorboards/new`}>
            <MenuItem eventKey="5">
              <i
                className="fas fa-play fa-sm icon"
                aria-hidden="true"
              /> Start tensorboard
            </MenuItem>
          </LinkContainer>
        </Dropdown.Menu>
      </Dropdown>
    </span>
    );
  }
}
