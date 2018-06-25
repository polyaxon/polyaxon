import * as React from 'react';

import * as actions from '../actions/build';
import PaginatedList from '../components/paginatedList';
import { EmptyList } from './emptyList';
import BuildHeader from './buildHeader';
import Build from './build';
import { BuildModel } from '../models/build';

export interface Props {
  build: BuildModel;
  fetchData: () => actions.BuildAction;
}

export default class EntityBuild extends React.Component<Props, Object> {
  componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const listBuilds = () => {
      if (this.props.build) {
        return (
          <ul>
            <li className="list-item">
              <Build build={this.props.build} onDelete={() => undefined}/>
            </li>
          </ul>
        );
      }
      return (null);
    };
    return (
      <PaginatedList
        count={this.props.build ? 1 : 0}
        componentList={listBuilds()}
        componentHeader={BuildHeader()}
        componentEmpty={EmptyList(false, 'build', 'build')}
        filters={false}
        fetchData={(offset: number, query?: string, sort?: string, extraFilters?: Object) => null}
      />
    );
  }
}
