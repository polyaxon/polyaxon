import * as React from 'react';
import * as _ from 'lodash';
import { Pager } from 'react-bootstrap';

import Experiment from './experiment';
import { ExperimentModel } from '../models/experiment';
import * as actions from '../actions/experiment';
import { paginate, paginateNext, paginatePrevious } from '../constants/paginate';

export interface Props {
  experiments: ExperimentModel[];
  count: number;
  onCreate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onUpdate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onDelete: (experiment: ExperimentModel) => actions.ExperimentAction;
  fetchData: (currentPage: number) => actions.ExperimentAction;
}

interface State {
  currentPage: number;
}

export default class Experiments extends React.Component<Props, State> {
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
    const experiments = this.props.experiments;
    return (
      <div className="row">
        <div className="col-md-12">
          <ul>
            {experiments.filter(
              (xp: ExperimentModel) => _.isNil(xp.deleted) || !xp.deleted
            ).map(
              (xp: ExperimentModel) =>
                <li className="list-item" key={xp.unique_name}>
                  <Experiment experiment={xp} onDelete={() => this.props.onDelete(xp)}/>
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
