import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';

import ConfirmAction from '../../../modals/confimAction';

import '../../../actions.less';

export interface Props {
  onDelete: () => any;
  onEdit: () => void;
  pullRight: boolean;
  isSelection?: boolean;
}

interface State {
  confirmShow: boolean;
  confirmComponent?: React.ReactNode;
  confirmAction?: 'delete' | 'edit';
}

export default class StoreActions extends React.Component<Props, State> {

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

  public handleShow = (action: 'delete') => {
    let confirmComponent: React.ReactNode = null;
    if (action === 'delete') {
      confirmComponent = this.props.isSelection ?
        (
          <div>
            <p>Are you sure you want to delete the selected <b>store(s)</b></p>
            <p><i className="fas fa-info-circle fa-alert"/> This action is irreversible!</p>
          </div>
        ) :
        (
          <div>
            <p>Are you sure you want to delete this <b>store</b></p>
            <p><i className="fas fa-info-circle fa-alert"/> This action is irreversible!</p>
          </div>
        );
    }
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{confirmShow: true, confirmAction: action, confirmComponent}
    }));
  };

  public confirm = () => {
    if (this.state.confirmAction === 'delete') {
      this.props.onDelete();
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
          <MenuItem eventKey="3" onClick={() => this.handleShow('delete')}>
            <i className="fas fa-trash icon" aria-hidden="true"/> Delete
          </MenuItem>
          <MenuItem eventKey="4" onClick={() => this.props.onEdit()}>
            <i className="fas fa-pen icon" aria-hidden="true"/> Edit
          </MenuItem>
        </Dropdown.Menu>
      </Dropdown>
      <ConfirmAction
        component={this.state.confirmComponent}
        confirmShow={this.state.confirmShow}
        onConfirm={() => this.confirm()}
        handleClose={() => this.handleClose()}
      />
    </span>
    );
  }
}
