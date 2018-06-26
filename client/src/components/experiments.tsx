import * as React from 'react';
import * as _ from 'lodash';
import { LinkContainer } from 'react-router-bootstrap';

import * as queryString from 'query-string';

import Experiment from './experiment';
import { ExperimentModel } from '../models/experiment';
import * as actions from '../actions/experiment';
import { EXPERIMENT_FILTERS } from './filters/constants';
import PaginatedList from './paginatedList';
import { EmptyList } from './emptyList';
import ExperimentHeader from './experimentHeader';
import GridList from './gridList';
import { getExperimentUrl, splitUniqueName } from '../constants/utils';

export interface Props {
  isCurrentUser: boolean;
  experiments: ExperimentModel[];
  count: number;
  onCreate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onUpdate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onDelete: (experiment: ExperimentModel) => actions.ExperimentAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.ExperimentAction;
}

export default class Experiments extends React.Component<Props, Object> {
  shouldComponentUpdate(nextProps: Props, nextState: Object) {
    let baseUrl = location.hash.split('?')[0];
    return baseUrl === '#experiments';
  }

  public render() {
    const getExperimentLink = (experimentName: string, experimentId: string | number) => {
      let values = splitUniqueName(experimentName);
      return(
        <LinkContainer to={getExperimentUrl(values[0], values[1], experimentId)}>
          <a className="title">
            <i className="fa fa-cube icon" aria-hidden="true"/>
            {experimentName}
          </a>
        </LinkContainer>
      );
    };

    const experiments = this.props.experiments;
    const listExperiments = () => {
      return (
        <ul>
          {experiments.filter(
            (xp: ExperimentModel) => _.isNil(xp.deleted) || !xp.deleted
          ).map(
            (xp: ExperimentModel) =>
              <li className="list-item" key={xp.unique_name}>
                <Experiment experiment={xp} onDelete={() => this.props.onDelete(xp)}/>
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

    let getListType = () => {
      let pieces = location.href.split('?');
      if (pieces.length > 1) {
        let search = queryString.parse(pieces[1]);
        if (search.metrics === true || search.metrics === 'true') {
          return 'metrics';
        } else if (search.declarations === true || search.declarations === 'true') {
          return 'declarations';
        }
      }
      return 'info';
    };
    const listType = getListType();

    let getList = () => {
      if (listType === 'metrics') {
        return listExperimentMetrics();
      } else if (listType === 'declarations') {
        return listExperimentDeclarations();
      }
      return listExperiments();
    };

    return (
      <PaginatedList
        count={this.props.count}
        componentList={getList()}
        componentHeader={listType === 'info' ? ExperimentHeader() : null}
        componentEmpty={EmptyList(
          this.props.isCurrentUser,
          'experiment',
          'experiment',
          'polyaxon run --help')
        }
        filters={EXPERIMENT_FILTERS}
        fetchData={this.props.fetchData}
      />
    );
  }
}
