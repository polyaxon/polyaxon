import * as React from 'react';
import { Modal } from 'react-bootstrap';

import '../actions.less';

export interface Props {
  btn?: string;
  component?: React.ReactNode;
  validation?: string;
  confirmShow: boolean;
  onConfirm: () => any;
  handleClose: () => void;
}

export interface State {
  validation: string;
}

export default class ConfirmAction extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      validation: ''
    };
  }

  public confirm = (event: any) => {
    event.preventDefault();
    this.props.onConfirm();
    this.props.handleClose();
  };

  public handleInputChange = (validation: string) => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      validation,
    }));
  };

  public render() {
    const btn = this.props.btn ? this.props.btn : 'btn-danger';
    const getConfirmButton = () => {
      if (this.props.validation) {
        return (
          <button
            role="button"
            type="submit"
            disabled={this.props.validation !== this.state.validation}
            className={`btn btn-default ${btn}`}
            onClick={this.confirm}
          >
            Confirm
          </button>
        );
      }
      return (
        <button
          role="button"
          type="submit"
          className={`btn btn-default ${btn}`}
          onClick={this.confirm}
        >
          Confirm
        </button>
      );
    };
    return (
      <Modal show={this.props.confirmShow} onHide={this.props.handleClose}>
        <Modal.Header closeButton={true}>
          <Modal.Title>Confirm action</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="row">
            <div className="col-md-12">
              {this.props.component ? this.props.component : <p>This action is irreversible</p>}
            </div>
          </div>
          <br/>
          {this.props.validation &&
          <div className="row">
            <div className="col-md-10">
              <div className="form-group">
                <label className="control-label">Please enter: <code>{this.props.validation}</code></label>
                <input
                  type="text"
                  className="form-control input-sm"
                  value={this.state.validation}
                  onChange={(event) => this.handleInputChange(event.target.value)}
                />
              </div>
            </div>
          </div>
          }
        </Modal.Body>
        <Modal.Footer>
          {getConfirmButton()}
        </Modal.Footer>
      </Modal>
    );
  }
}
