import * as React from 'react';
import * as _ from 'lodash';

import Group from './group';
import { GroupModel } from '../models/group';
import {paginate, paginateNext, paginatePrevious} from '../constants/paginate';
import {Pager} from 'react-bootstrap';

export interface Props {
  groups: GroupModel[];
  count: number;
  onCreate: (group: GroupModel) => any;
  onUpdate: (group: GroupModel) => any;
  onDelete: (group: GroupModel) => any;
  fetchData: (currentPage: number) => any;
}

interface State {
  currentPage: number;
}

export default class Groups extends React.Component<Props, State> {
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
  };

  handlePreviousPage = () => {
      this.setState((prevState, prevProps) => ({
        currentPage: prevState.currentPage - 1,
      }));
  };

  public render() {
    const groups = this.props.groups;
    return (
      <div className="row">
        <div className="col-md-12">
          <ul>
            {groups.filter(
              (group: GroupModel) => _.isNil(group.deleted) || !group.deleted
            ).map(
              (group: GroupModel) =>
                <li className="list-item" key={group.unique_name}>
                  <Group group={group} onDelete={() => this.props.onDelete(group)}/>
                </li>)}
          </ul>
        </div>
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
