import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';

import { ActionInterface } from '../../interfaces/actions';
import ConfirmAction from '../modals/confimAction';

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

interface State {
  confirmShow: boolean;
  confirmText?: string;
  confirmAction?: 'delete' | 'stop' | 'stopTensorboard';
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

  public handleShow = (action: 'delete' | 'stop' | 'stopTensorboard') => {
    let confirmText = '';
    if (action === 'delete') {
      confirmText = 'Are you sure you want to delete this experiment';
    } else if (action === 'stop') {
      confirmText = 'Are you sure you want to stop this experiment';
    } else if (action === 'stopTensorboard') {
      confirmText = 'Are you sure you want to stop tensorboard for this experiment';
    }
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{confirmShow: true, confirmAction: action, confirmText}
    }));
  };

  public confirm = () => {
    if (this.state.confirmAction === 'delete') {
      this.props.onDelete();
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
            <i className="fa fa-ellipsis-h icon" aria-hidden="true"/>
        </Dropdown.Toggle>
        <Dropdown.Menu>
          {actions.map((action: ActionInterface, idx: number) => (
            <MenuItem key={idx} eventKey="1" onClick={action.callback}>
              <i className={`fa fa-${action.icon} icon`} aria-hidden="true"/> {action.name}
            </MenuItem>
          ))}
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
