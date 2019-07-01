import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

import { ActionInterface } from '../../interfaces/actions';
import ConfirmAction from '../modals/confimAction';

import '../actions.less';

export interface Props {
  onDelete: () => any;
  onStop: () => any;
  onArchive?: () => any;
  onRestore?: () => any;
  onRestart?: () => any;
  onResume?: () => any;
  tensorboardActionCallback?: () => any;
  hasTensorboard?: boolean;
  isRunning: boolean;
  pullRight: boolean;
  experimentUrl?: string;
  isSelection?: boolean;
  actions?: ActionInterface[];
}

interface State {
  confirmShow: boolean;
  confirmText?: string;
  confirmAction?: 'delete' | 'stop' | 'stopTensorboard' | 'archive';
}

export default class ExperimentActions extends React.Component<Props, State> {

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
        'Are you sure you want to delete the selected experiment(s)' :
        'Are you sure you want to delete this experiment';
    } else if (action === 'archive') {
      confirmText = this.props.isSelection ?
        'Are you sure you want to archive the selected experiment(s)' :
        'Are you sure you want to archive this experiment';
    } else if (action === 'stop') {
      confirmText = this.props.isSelection ?
        'Are you sure you want to stop the selected experiment(s)' :
        'Are you sure you want to stop this experiment';
    } else if (action === 'stopTensorboard') {
      confirmText = this.props.isSelection ?
        'Are you sure you want to stop tensorboard for the selected experiment(s)' :
        'Are you sure you want to stop tensorboard for this experiment';
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
    } else if (this.state.confirmAction === 'stop') {
      this.props.onStop();
    } else if (this.state.confirmAction === 'stopTensorboard' && this.props.tensorboardActionCallback) {
      this.props.tensorboardActionCallback();
    }
  };

  public render() {
    const actions = this.props.actions || [];
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
          {actions.map((action: ActionInterface, idx: number) => (
            <MenuItem key={idx} eventKey="1" onClick={action.callback}>
              <i className={`${action.icon} icon`} aria-hidden="true"/> {action.name}
            </MenuItem>
          ))}
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
          {this.props.onResume && !this.props.isRunning &&
          <MenuItem eventKey="2" onClick={this.props.onResume}>
            <i className="fas fa-reply icon" aria-hidden="true"/> Resume
          </MenuItem>
          }
          {this.props.tensorboardActionCallback && this.props.hasTensorboard &&
          <MenuItem eventKey="3" onClick={() => this.handleShow('stopTensorboard')}>
            <i
              className="fas fa-stop icon"
              aria-hidden="true"
            /> Stop Tensorboard
          </MenuItem>
          }
          {!this.props.hasTensorboard && this.props.experimentUrl &&
          <LinkContainer to={`${this.props.experimentUrl}/tensorboards/new`}>
            <MenuItem eventKey="4" onClick={() => this.handleShow('stopTensorboard')}>
              <i
                className="fas fa-play fa-sm icon"
                aria-hidden="true"
              /> Start Tensorboard
            </MenuItem>
          </LinkContainer>
          }
          {this.props.onRestore &&
          <MenuItem eventKey="5" onClick={this.props.onRestore}>
            <i className="fas fa-recycle icon" aria-hidden="true"/> Restore
          </MenuItem>
          }
          {this.props.onArchive &&
          <MenuItem eventKey="6" onClick={() => this.handleShow('archive')}>
            <i className="fas fa-archive icon" aria-hidden="true"/> Archive
          </MenuItem>
          }
          <MenuItem eventKey="7" onClick={() => this.handleShow('delete')}>
          <i className="fas fa-trash icon" aria-hidden="true"/> Delete
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
