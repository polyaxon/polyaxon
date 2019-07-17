import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';

import ConfirmAction from '../modals/confimAction';

import '../actions.less';

export interface Props {
  onDelete: () => any;
  onStop?: () => any;
  onRestart?: () => any;
  onArchive?: () => any;
  onRestore?: () => any;
  isRunning: boolean;
  pullRight: boolean;
  isSelection?: boolean;
}

interface State {
  confirmShow: boolean;
  confirmComponent?: React.ReactNode;
  confirmAction?: 'delete' | 'stop' | 'archive';
}

export default class JobActions extends React.Component<Props, State> {

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

  public handleShow = (action: 'delete' | 'stop' | 'archive') => {
    let confirmComponent: React.ReactNode = null;
    if (action === 'delete') {
      confirmComponent = this.props.isSelection ?
        (
          <div>
            <p>Are you sure you want to delete the selected <b>job(s)</b></p>
            <p><i className="fas fa-info-circle fa-alert"/> This action is irreversible!</p>
          </div>
        ) :
        (
          <div>
            <p>Are you sure you want to delete this <b>job</b></p>
            <p><i className="fas fa-info-circle fa-alert"/> This action is irreversible!</p>
          </div>
        );
    } else if (action === 'archive') {
      confirmComponent = this.props.isSelection ?
        <p>Are you sure you want to archive the selected <b>job(s)</b></p> :
        <p>Are you sure you want to archive this <b>job</b></p>;
    } else if (action === 'stop') {
      confirmComponent = this.props.isSelection ?
        <p>Are you sure you want to stop the selected <b>job(s)</b></p> :
        <p>Are you sure you want to stop this <b>job</b></p>;
    }
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{confirmShow: true, confirmAction: action, confirmComponent}
    }));
  };

  public confirm = () => {
    if (this.state.confirmAction === 'delete') {
      this.props.onDelete();
    } else if (this.state.confirmAction === 'archive' && this.props.onArchive) {
      this.props.onArchive();
    } else if (this.state.confirmAction === 'stop' && this.props.onStop) {
      this.props.onStop();
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
          {this.props.onStop && this.props.isRunning &&
          <MenuItem eventKey="1" onClick={() => this.handleShow('stop')}>
            <i className="fas fa-stop icon" aria-hidden="true"/> Stop
          </MenuItem>
          }
          {this.props.onRestart && !this.props.isRunning &&
          <MenuItem eventKey="1" onClick={this.props.onRestart}>
            <i className="fas fa-redo icon" aria-hidden="true"/> Restart
          </MenuItem>
          }
          {this.props.onRestore &&
          <MenuItem eventKey="1" onClick={this.props.onRestore}>
            <i className="fas fa-recycle icon" aria-hidden="true"/> Restore
          </MenuItem>
          }
          {this.props.onArchive &&
          <MenuItem eventKey="1" onClick={() => this.handleShow('archive')}>
            <i className="fas fa-archive icon" aria-hidden="true"/> Archive
          </MenuItem>
          }
          <MenuItem eventKey="2" onClick={() => this.handleShow('delete')}>
          <i className="fas fa-trash icon" aria-hidden="true"/> Delete
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
