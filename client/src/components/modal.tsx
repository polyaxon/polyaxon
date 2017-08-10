import * as React from "react";
import {Button, Modal} from "react-bootstrap";
import {ModalStateSchema} from "../models/modal";


export interface Props {
  modalProps: ModalStateSchema;
  hideModal: () => any
}

function RootModal({modalProps, hideModal}: Props) {
  return (
      <Modal show={modalProps.props.show} onHide={hideModal} bsSize="small" aria-labelledby="contained-modal-title-sm">
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-sm">Modal heading</Modal.Title>
        </Modal.Header>
        <Modal.Body>

        </Modal.Body>
        <Modal.Footer>
          <Button onClick={hideModal}>Close</Button>
        </Modal.Footer>
      </Modal>
    );
};


export default RootModal;
