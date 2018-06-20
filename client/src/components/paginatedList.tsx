import * as React from 'react';
import { Pager } from 'react-bootstrap';

import { paginate, paginateNext, paginatePrevious } from '../constants/paginate';
import './paginatedList.less';

export interface Props {
  count: number;
  componentList: React.ReactNode;
  fetchData: (currentPage: number) => any;
}

interface State {
  currentPage: number;
}

export default class PaginatedList extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {currentPage: 1};
  }

  componentDidMount() {
    this.props.fetchData(this.state.currentPage);
  }

  componentDidUpdate(prevProps: Props, prevState: State) {
    if (this.state.currentPage !== prevState.currentPage) {
      this.props.fetchData(this.state.currentPage);
    }
  }

  handleNextPage = () => {
      this.setState((prevState, prevProps) => ({
        currentPage: prevState.currentPage + 1,
      }));
  }

  handlePreviousPage = () => {
      this.setState((prevState, prevProps) => ({
        currentPage: prevState.currentPage - 1,
      }));
  }

  public render() {
    return (
      <div className="row paginated-list">
        {this.props.componentList}
        {paginate(this.props.count) &&
        <Pager>
          <Pager.Item
            onClick={this.handlePreviousPage}
            disabled={!paginatePrevious(this.state.currentPage)}
          >
            Previous
          </Pager.Item>{' '}
          <Pager.Item
            onClick={this.handleNextPage}
            disabled={!paginateNext(this.state.currentPage, this.props.count)}
          >
            Next
          </Pager.Item>
        </Pager>
        }
      </div>
    );
  }
}
