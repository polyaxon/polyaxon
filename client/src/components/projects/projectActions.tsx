import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';

import ConfirmAction from '../modals/confimAction';

import '../actions.less';

export interface Props {
  onDelete: () => any;
  notebookActionCallback?: () => any;
  tensorboardActionCallback?: () => any;
  hasNotebook?: boolean;
  hasTensorboard?: boolean;
  pullRight: boolean;
}

interface State {
  confirmShow: boolean;
  confirmText?: string;
  confirmAction?: 'delete' | 'stopNotebook' | 'stopTensorboard';
}

export default class ProjectActions extends React.Component<Props, State> {

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

  public handleShow = (action: 'delete' | 'stopNotebook' | 'stopTensorboard') => {
    let confirmText = '';
    if (action === 'delete') {
      confirmText = 'Are you sure you want to delete this project';
    } else if (action === 'stopNotebook') {
      confirmText = 'Are you sure you want to stop notebook for this project';
    } else if (action === 'stopTensorboard') {
      confirmText = 'Are you sure you want to stop tensorboard for this project';
    }
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{confirmShow: true, confirmAction: action, confirmText}
    }));
  };

  public confirm = () => {
    if (this.state.confirmAction === 'delete') {
      this.props.onDelete();
    } else if (this.state.confirmAction === 'stopNotebook' && this.props.notebookActionCallback) {
      this.props.notebookActionCallback();
    } else if (this.state.confirmAction === 'stopTensorboard' && this.props.tensorboardActionCallback) {
      this.props.tensorboardActionCallback();
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
            <i className="fa fa-ellipsis-h icon" aria-hidden="true"/>
        </Dropdown.Toggle>
        <Dropdown.Menu>
          {this.props.notebookActionCallback && this.props.hasNotebook &&
          <MenuItem eventKey="2" onClick={() => this.handleShow('stopNotebook')}>
            <i
              className="fa fa-stop icon"
              aria-hidden="true"
            /> Stop Notebook
          </MenuItem>
          }
          {this.props.tensorboardActionCallback && this.props.hasTensorboard &&
          <MenuItem eventKey="2" onClick={() => this.handleShow('stopTensorboard')}>
            <i
              className="fa fa-stop icon"
              aria-hidden="true"
            /> Stop Tensorboard
          </MenuItem>
          }
          <MenuItem eventKey="2" onClick={() => this.handleShow('delete')}>
            <i className="fa fa-trash icon" aria-hidden="true"/> Delete
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
