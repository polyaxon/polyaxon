import * as React from 'react';
import { Modal } from 'react-bootstrap';

import * as actions from '../../../../actions/stores';
import StoreFrom from '../../../../containers/settings/catalogs/storeForm';
import { StoreModel } from '../../../../models/store';
import { isLive } from '../../../../utils/isLive';
import { EmptyList } from '../../../empty/emptyList';
import PaginatedTable from '../../../tables/paginatedTable';
import CatalogsSidebar from '../sidebar';
import Store from './store';
import StoreHeader from './storeHeader';

import '../../../actions.less';
import '../../settings.less';

export interface Props {
  resource: string;
  stores: StoreModel[];
  count: number;
  isLoading: boolean;
  errors: any;
  showDeleted: boolean;
  onFetch: () => actions.StoreAction;
  onDelete: (name: string) => actions.StoreAction;
}

export interface State {
  showModal: boolean;
  store?: StoreModel;
}

export default class Stores extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      showModal: false,
      store: undefined,
    };
  }

  public componentDidMount() {
    this.props.onFetch();
  }

  public handleClose = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState, showModal: false
    }));
  };

  public handleShow = (store?: StoreModel) => {
    this.setState((prevState, prevProps) => ({
      ...prevState, showModal: true, store: store || undefined
    }));
  };

  public render() {
    const listStores = () => {
      return (
        <table className="table table-hover table-responsive">
          <tbody>
          {StoreHeader()}
          {this.props.stores
            .filter(
              (store: StoreModel) =>
                (!this.props.showDeleted && isLive(store)) || (this.props.showDeleted && !isLive(store)))
            .map(
              (store: StoreModel) =>
                <Store
                  key={store.uuid}
                  resource={this.props.resource}
                  store={store}
                  onDelete={() => this.props.onDelete(store.name)}
                  onEdit={() => this.handleShow(store)}
                />)}
          </tbody>
        </table>
      );
    };

    const StoreModal = (
      <Modal show={this.state.showModal} onHide={this.handleClose}>
        <Modal.Header closeButton={true}>
          <Modal.Title>{this.state.store ? 'Update Store' : 'Create New Store'}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <StoreFrom
            resource={this.props.resource}
            cstore={this.state.store}
            onCancel={this.handleClose}
          />
        </Modal.Body>
      </Modal>
    );

    return (
      <div className="row settings">
        <div className="col-md-3">
          <CatalogsSidebar/>
        </div>
        <div className="col-md-9">
          <h3 className="menu-header">
            {this.props.resource}
            <span className="actions pull-right">
              <button
                type="button"
                className="btn btn-sm btn-success"
                onClick={() => this.handleShow()}
              >
                <i className="fas fa-plus fa-sm icon"/> New
              </button>
            </span>
          </h3>
          <PaginatedTable
            isLoading={this.props.isLoading}
            errors={this.props.errors}
            count={this.props.count}
            componentList={listStores()}
            componentEmpty={EmptyList(false, this.props.resource, '')}
            filters={false}
            fetchData={this.props.onFetch}
          />
        </div>
        {StoreModal}
      </div>
    );
  }
}
