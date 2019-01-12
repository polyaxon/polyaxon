import * as React from 'react';
import { Dropdown, MenuItem, Modal } from 'react-bootstrap';

import '../actions.less';

export interface Props {
  text?: string;
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
    return (
      <Modal show={this.props.confirmShow} onHide={this.props.handleClose}>
        <Modal.Header closeButton={true}>
          <Modal.Title>Confirm action</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>{this.props.text || `This action is irreversible`}</p>
        </Modal.Body>
        <Modal.Footer>
          <button type="submit" className="btn btn-default btn-danger" onClick={this.confirm}>Confirm</button>
        </Modal.Footer>
      </Modal>
    );
  }
}
