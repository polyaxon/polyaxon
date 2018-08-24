import * as React from 'react';

import * as actions from '../actions/build';
import PaginatedTable from '../components/paginatedTable';
import { BuildModel } from '../models/build';
import Build from './build';
import BuildHeader from './buildHeader';
import { EmptyList } from './empty/emptyList';

export interface Props {
  build: BuildModel;
  fetchData: () => actions.BuildAction;
  onDelete: (buildName: string) => actions.BuildAction;
  onStop: (buildName: string) => actions.BuildAction;
}

export default class EntityBuild extends React.Component<Props, Object> {
  public componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const listBuilds = () => {
      if (this.props.build) {
        return (
          <tbody>
          {BuildHeader()}
          <Build
            build={this.props.build}
            onDelete={() => this.props.onDelete(this.props.build.unique_name)}
            onStop={() => this.props.onStop(this.props.build.unique_name)}
          />
          </tbody>
        );
      }
      return (null);
    };
    return (
      <PaginatedTable
        count={this.props.build ? 1 : 0}
        componentList={listBuilds()}
        componentEmpty={EmptyList(false, 'build', 'build')}
        filters={false}
        fetchData={(offset: number, query?: string, sort?: string, extraFilters?: Object) => null}
      />
    );
  }
}
