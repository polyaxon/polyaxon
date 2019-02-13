import * as React from 'react';

import * as actions from '../../actions/build';
import { BuildModel } from '../../models/build';
import { EmptyList } from '../empty/emptyList';
import PaginatedTable from '../tables/paginatedTable';
import Build from './build';
import BuildHeader from './buildHeader';

export interface Props {
  build: BuildModel;
  fetchData: () => actions.BuildAction;
  onDelete: (buildName: string) => actions.BuildAction;
  onStop: (buildName: string) => actions.BuildAction;
  onArchive: (buildName: string) => actions.BuildAction;
  onRestore: (buildName: string) => actions.BuildAction;
  showBookmarks: boolean;
  bookmark: (buildName: string) => actions.BuildAction;
  unbookmark: (buildName: string) => actions.BuildAction;
}

export default class EntityBuild extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const listBuilds = () => {
      if (this.props.build) {
        return (
          <table className="table table-hover table-responsive">
            <tbody>
            {BuildHeader()}
            <Build
              build={this.props.build}
              onDelete={() => this.props.onDelete(this.props.build.unique_name)}
              onStop={() => this.props.onStop(this.props.build.unique_name)}
              onArchive={() => this.props.onArchive(this.props.build.unique_name)}
              onRestore={() => this.props.onRestore(this.props.build.unique_name)}
              bookmark={() => this.props.bookmark(this.props.build.unique_name)}
              unbookmark={() => this.props.unbookmark(this.props.build.unique_name)}
              showBookmarks={this.props.showBookmarks}
            />
            </tbody>
          </table>
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
        fetchData={(offset: number, query?: string, sort?: string, extraFilters?: {}) => null}
      />
    );
  }
}
