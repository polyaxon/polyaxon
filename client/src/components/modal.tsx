import * as React from "react";
import {Button, Modal} from "react-bootstrap";

import CreateProjectForm from "./createProjectForm";
import {ModalStateSchema, modalTypes} from "../models/modal";


export interface Props {
  modalProps: ModalStateSchema;
  hideModal: () => any
}

function RootModal({modalProps, hideModal}: Props) {
  let bodyComponent;
  switch (modalProps.type) {
    case modalTypes.CREATE_PROJECT:
      bodyComponent = <CreateProjectForm onSubmit={(values) => {
        modalProps.props.submitCb({
          ...values,
          id: 100,
          createdAt: new Date(),
          updatedAt: new Date()
        });
        hideModal();
      }}/>
  }

  let footer = null;
  if (modalProps.props.showFooter) {
    footer = <Modal.Footer><Button onClick={hideModal}>Close</Button></Modal.Footer>
  }

  return (
    <Modal show={modalProps.props.show} onHide={hideModal} bsSize="small"
           aria-labelledby="contained-modal-title-sm">
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-sm">{modalProps.props.heading}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {bodyComponent}
      </Modal.Body>
      {footer}
    </Modal>
  );
};


export default RootModal;
