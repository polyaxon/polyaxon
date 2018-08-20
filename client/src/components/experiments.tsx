import * as _ from 'lodash';
import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import * as queryString from 'query-string';

import * as actions from '../actions/experiment';
import { getExperimentUrl, splitUniqueName } from '../constants/utils';
import { ExperimentModel } from '../models/experiment';
import { EmptyBookmarks } from './empty/emptyBookmarks';
import { EmptyList } from './empty/emptyList';
import Experiment from './experiment';
import ExperimentHeader from './experimentHeader';
import { EXPERIMENT_FILTERS } from './filters/constants';
import GridList from './gridList';
import PaginatedList from './paginatedList';

export interface Props {
  isCurrentUser: boolean;
  experiments: ExperimentModel[];
  count: number;
  useFilters: boolean;
  bookmarks: boolean;
  onCreate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onUpdate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onDelete: (experimentName: string) => actions.ExperimentAction;
  onStop: (experimentName: string) => actions.ExperimentAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.ExperimentAction;
}

export default class Experiments extends React.Component<Props, Object> {
  public shouldComponentUpdate(nextProps: Props, nextState: Object) {
    const baseUrl = location.hash.split('?')[0];
    return baseUrl === '#experiments';
  }

  public render() {
    const getExperimentLink = (experimentName: string, experimentId: string | number) => {
      const values = splitUniqueName(experimentName);
      return(
        <LinkContainer to={getExperimentUrl(values[0], values[1], experimentId)}>
          <a className="title">
            <i className="fa fa-cube icon" aria-hidden="true"/>
            {experimentName}
          </a>
        </LinkContainer>
      );
    };

    const filters = this.props.useFilters ? EXPERIMENT_FILTERS : false;
    const experiments = this.props.experiments;
    const listExperiments = () => {
      return (
        <ul>
          {experiments.filter(
            (xp: ExperimentModel) => _.isNil(xp.deleted) || !xp.deleted
          ).map(
            (xp: ExperimentModel) =>
              <li className="list-item" key={xp.unique_name}>
                <Experiment
                  experiment={xp}
                  onDelete={() => this.props.onDelete(xp.unique_name)}
                  onStop={() => this.props.onStop(xp.unique_name)}
                />
              </li>)}
        </ul>
      );
    };
    const listExperimentMetrics = () => {
      return (
        <GridList
          rows={experiments
            .filter((xp: ExperimentModel) => xp.last_metric)
            .map((xp: ExperimentModel) => (
              {
                ...{experiment: getExperimentLink(xp.unique_name, xp.id)},
                ...xp.last_metric
              }))}
        />
      );
    };

    const listExperimentDeclarations = () => {
      return (
        <GridList
          rows={experiments
            .filter((xp: ExperimentModel) => xp.declarations)
            .map((xp: ExperimentModel) => (
              {
                ...{experiment: getExperimentLink(xp.unique_name, xp.id)},
                ...xp.declarations
              }))}
        />
      );
    };

    const getListType = () => {
      const pieces = location.href.split('?');
      if (pieces.length > 1) {
        const search = queryString.parse(pieces[1]);
        if (search.metrics === true || search.metrics === 'true') {
          return 'metrics';
        } else if (search.declarations === true || search.declarations === 'true') {
          return 'declarations';
        }
      }
      return 'info';
    };
    const listType = getListType();

    const getList = () => {
      if (listType === 'metrics') {
        return listExperimentMetrics();
      } else if (listType === 'declarations') {
        return listExperimentDeclarations();
      }
      return listExperiments();
    };

    const empty = this.props.bookmarks ?
      EmptyBookmarks(
        this.props.isCurrentUser,
        'experiment',
        'experiment')
      : EmptyList(
        this.props.isCurrentUser,
        'experiment',
        'experiment',
        'polyaxon run --help');
    return (
      <PaginatedList
        count={this.props.count}
        componentList={getList()}
        componentHeader={listType === 'info' ? ExperimentHeader() : null}
        componentEmpty={empty}
        filters={filters}
        fetchData={this.props.fetchData}
      />
    );
  }
}
