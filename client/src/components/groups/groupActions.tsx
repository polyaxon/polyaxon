import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';

import ConfirmAction from '../modals/confimAction';

import '../actions.less';

export interface Props {
  onDelete: () => any;
  onStop?: () => any;
  onArchive?: () => any;
  onRestore?: () => any;
  tensorboardActionCallback?: () => any;
  hasTensorboard?: boolean;
  isRunning: boolean;
  pullRight: boolean;
  isSelection?: boolean;
}

interface State {
  confirmShow: boolean;
  confirmText?: string;
  confirmAction?: 'delete' | 'stop' | 'stopTensorboard' | 'archive';
}

export default class GroupActions extends React.Component<Props, State> {

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

  public handleShow = (action: 'delete' | 'stop' | 'stopTensorboard' | 'archive') => {
    let confirmText = '';
    if (action === 'delete') {
      confirmText = this.props.isSelection ?
        'Are you sure you want to delete the selected group(s)' :
        'Are you sure you want to delete this group';
    } else if (action === 'archive') {
      confirmText = this.props.isSelection ?
        'Are you sure you want to archive the selected group(s)' :
        'Are you sure you want to archive this group';
    } else if (action === 'stop') {
      confirmText = this.props.isSelection ?
        'Are you sure you want to stop the selected group(s)' :
        'Are you sure you want to stop this group';
    } else if (action === 'stopTensorboard') {
      confirmText = this.props.isSelection ?
        'Are you sure you want to stop tensorboard for the selected group(s)' :
        'Are you sure you want to stop tensorboard for this group';
    }
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{confirmShow: true, confirmAction: action, confirmText}
    }));
  };

  public confirm = () => {
    if (this.state.confirmAction === 'delete') {
      this.props.onDelete();
    } else if (this.state.confirmAction === 'archive' && this.props.onArchive) {
      this.props.onArchive();
    } else if (this.state.confirmAction === 'stop' && this.props.onStop) {
      this.props.onStop();
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
          {this.props.onStop && this.props.isRunning &&
          <MenuItem eventKey="1" onClick={() => this.handleShow('stop')}>
            <i className="fa fa-stop icon" aria-hidden="true"/> Stop
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
          {this.props.onRestore &&
          <MenuItem eventKey="1" onClick={this.props.onRestore}>
            <i className="fa fa-recycle icon" aria-hidden="true"/> Restore
          </MenuItem>
          }
          {this.props.onArchive &&
          <MenuItem eventKey="1" onClick={() => this.handleShow('archive')}>
            <i className="fa fa-archive icon" aria-hidden="true"/> Archive
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
