import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';

import ConfirmAction from '../modals/confimAction';

import '../actions.less';

export interface Props {
  onDelete: () => any;
  onArchive?: () => any;
  onRestore?: () => any;
  notebookActionCallback?: () => any;
  tensorboardActionCallback?: () => any;
  hasNotebook?: boolean;
  hasTensorboard?: boolean;
  pullRight: boolean;
  isSelection?: boolean;
}

interface State {
  confirmShow: boolean;
  confirmComponent?: React.ReactNode;
  confirmAction?: 'delete' | 'stopNotebook' | 'stopTensorboard' | 'archive';
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

  public handleShow = (action: 'delete' | 'stopNotebook' | 'stopTensorboard' | 'archive') => {
    let confirmComponent: React.ReactNode = null;
    if (action === 'delete') {
      confirmComponent = this.props.isSelection ?
        (
          <div>
            <p>Are you sure you want to delete the selected <b>project(s)</b></p>
            <p><i className="fas fa-info-circle fa-alert"/> This action is irreversible!</p>
          </div>
        ) :
        (
          <div>
            <p>Are you sure you want to delete this <b>project</b></p>
            <p><i className="fas fa-info-circle fa-alert"/> This action is irreversible!</p>
          </div>
        );
    } else if (action === 'archive') {
      confirmComponent = this.props.isSelection ?
        <p>Are you sure you want to archive the selected <b>project(s)</b></p> :
        <p>Are you sure you want to archive this <b>project</b></p>;
    } else if (action === 'stopNotebook') {
      confirmComponent = this.props.isSelection ?
        <p>Are you sure you want to stop notebook for the selected <b>project(s)</b></p> :
        <p>Are you sure you want to stop notebook for this <b>project</b></p>;
    } else if (action === 'stopTensorboard') {
      confirmComponent = this.props.isSelection ?
        <p>Are you sure you want to stop tensorboard for the selected <b>project(s)</b></p> :
        <p>Are you sure you want to stop tensorboard for this <b>project</b></p>;
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
            <i className="fas fa-ellipsis-h icon" aria-hidden="true"/>
        </Dropdown.Toggle>
        <Dropdown.Menu>
          {this.props.notebookActionCallback && this.props.hasNotebook &&
          <MenuItem eventKey="2" onClick={() => this.handleShow('stopNotebook')}>
            <i
              className="fas fa-stop icon"
              aria-hidden="true"
            /> Stop Notebook
          </MenuItem>
          }
          {this.props.tensorboardActionCallback && this.props.hasTensorboard &&
          <MenuItem eventKey="2" onClick={() => this.handleShow('stopTensorboard')}>
            <i
              className="fas fa-stop icon"
              aria-hidden="true"
            /> Stop Tensorboard
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
