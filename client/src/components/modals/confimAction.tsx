import * as React from 'react';
import { Dropdown, MenuItem, Modal } from 'react-bootstrap';

import '../actions.less';

export interface Props {
  btn?: string;
  component?: React.ReactNode;
  confirmShow: boolean;
  onConfirm: () => any;
  handleClose: () => void;
}

export default class ConfirmAction extends React.Component<Props, {}> {

  public confirm = (event: any) => {
    event.preventDefault();
    this.props.onConfirm();
    this.props.handleClose();
  };

  public render() {
    const btn = this.props.btn ? this.props.btn : 'btn-danger';
    return (
      <Modal show={this.props.confirmShow} onHide={this.props.handleClose}>
        <Modal.Header closeButton={true}>
          <Modal.Title>Confirm action</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {this.props.component ? this.props.component : <p>This action is irreversible</p>}
        </Modal.Body>
        <Modal.Footer>
          <button type="submit" className={`btn btn-default ${btn}`} onClick={this.confirm}>Confirm</button>
        </Modal.Footer>
      </Modal>
    );
  }
}
