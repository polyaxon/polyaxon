import * as React from 'react';
import { Modal } from 'react-bootstrap';

import * as actions from '../../actions/statuses';
import { StatusModel } from '../../models/status';
import { EmptyList } from '../empty/emptyList';
import PaginatedList from '../tables/paginatedList';
import StatusHeader from './statusHeader';
import StatusItem from './statusItem';

import './statuses.less';

export interface Props {
  statuses: StatusModel[];
  count: number;
  fetchData: () => actions.StatusesAction;
}

interface State {
  showStatusModal: boolean;
  currentStatus?: StatusModel;
}

export default class Statuses extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      showStatusModal: false
    };
  }

  public handleClose = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{showStatusModal: false}
    }));
  };

  public handleShow = (status: StatusModel) => {
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{showStatusModal: true, currentStatus: status}
    }));
  };

  public render() {
    const statuses = this.props.statuses;
    const listStatuses = () => {
      return (
        <ul>
          {statuses.map(
            (status: StatusModel) =>
              <li className="list-item status-item" key={status.id}>
                <StatusItem status={status} onClick={() => this.handleShow(status)}/>
              </li>)}
        </ul>
      );
    };
    return (
      <div>
        <PaginatedList
          count={this.props.count}
          componentList={listStatuses()}
          componentHeader={StatusHeader()}
          componentEmpty={
            EmptyList(
              false,
              'status',
              'status')}
          filters={false}
          fetchData={this.props.fetchData}
        />
        <Modal show={this.state.showStatusModal} onHide={this.handleClose}>
          <Modal.Header closeButton={true}>
            <Modal.Title>Status details</Modal.Title>
          </Modal.Header>
          <Modal.Body className="status-details">
            <div className="traceback">
              <p>{this.state.currentStatus && this.state.currentStatus.traceback}</p>
            </div>
          </Modal.Body>
        </Modal>
      </div>
    );
  }
}
