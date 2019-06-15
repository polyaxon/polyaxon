import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';

import ConfirmAction from '../../../modals/confimAction';

import '../../../actions.less';

export interface Props {
  onDelete: () => any;
  onMakeDefault: () => any;
  onEdit: () => void;
  pullRight: boolean;
  isSelection?: boolean;
}

interface State {
  confirmShow: boolean;
  confirmText?: string;
  confirmAction?: 'delete' | 'default';
}

export default class AccessActions extends React.Component<Props, State> {

  constructor(props: Props) {
    super(props);
    this.state = {
      confirmShow: false,
    };
  }

   public handleClose = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{confirmShow: false}
    }));
  };

  public handleShow = (action: 'delete' | 'default') => {
    let confirmText = '';
    if (action === 'delete') {
      confirmText = this.props.isSelection ?
        'Are you sure you want to delete the selected access(es)' :
        'Are you sure you want to delete this access';
    } else if  (action === 'default') {
      confirmText = 'Are you sure you want to make this access the default';
    }
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{confirmShow: true, confirmAction: action, confirmText}
    }));
  };

  public confirm = () => {
    if (this.state.confirmAction === 'delete') {
      this.props.onDelete();
    } else if (this.state.confirmAction === 'default') {
      this.props.onMakeDefault();
    }
  };

  public render() {
    return (
      <span className={this.props.pullRight ? 'actions pull-right' : 'actions'}>
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
            <i className="fas fa-ellipsis-h icon" aria-hidden="true"/>
        </Dropdown.Toggle>
        <Dropdown.Menu>
          <MenuItem eventKey="2" onClick={() => this.handleShow('default')}>
            <i className="fas fa-check icon" aria-hidden="true"/> Make default
          </MenuItem>
          <MenuItem eventKey="3" onClick={() => this.handleShow('delete')}>
            <i className="fas fa-trash icon" aria-hidden="true"/> Delete
          </MenuItem>
          <MenuItem eventKey="4" onClick={() => this.props.onEdit()}>
            <i className="fas fa-pen icon" aria-hidden="true"/> Edit
          </MenuItem>
        </Dropdown.Menu>
      </Dropdown>
      <ConfirmAction
        text={this.state.confirmText}
        confirmShow={this.state.confirmShow}
        onConfirm={() => this.confirm()}
        handleClose={() => this.handleClose()}
      />
    </span>
    );
  }
}
