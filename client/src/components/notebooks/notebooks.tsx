import * as React from 'react';

import * as actions from '../../actions/notebooks';
import * as search_actions from '../../actions/search';
import { JOB_FILTER_OPTIONS } from '../../constants/filtering';
import { DEFAULT_SORT_OPTIONS } from '../../constants/sorting';
import { NotebookModel } from '../../models/notebook';
import { SearchModel } from '../../models/search';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { isLive } from '../../utils/isLive';
import { EmptyArchives } from '../empty/emptyArchives';
import { EmptyBookmarks } from '../empty/emptyBookmarks';
import { EmptyList } from '../empty/emptyList';
import { DEFAULT_FILTERS } from '../filters/constants';
import PaginatedTable from '../tables/paginatedTable';
import Notebook from './notebook';
import NotebookHeader from './notebookHeader';

export interface Props {
  isCurrentUser: boolean;
  notebooks: NotebookModel[];
  count: number;
  useFilters: boolean;
  showBookmarks: boolean;
  showDeleted: boolean;
  endpointList: string;
  onUpdate: (notebook: NotebookModel) => actions.NotebookAction;
  onDelete: (notebookName: string) => actions.NotebookAction;
  onStop: (notebookName: string) => actions.NotebookAction;
  onArchive: (notebookName: string) => actions.NotebookAction;
  onRestore: (notebookName: string) => actions.NotebookAction;
  bookmark: (notebookName: string) => actions.NotebookAction;
  unbookmark: (notebookName: string) => actions.NotebookAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.NotebookAction;
  fetchSearches?: () => search_actions.SearchAction;
  createSearch?: (data: SearchModel) => search_actions.SearchAction;
  deleteSearch?: (searchId: number) => search_actions.SearchAction;
}

export default class Notebooks extends React.Component<Props, {}> {
  public render() {
    const filters = this.props.useFilters ? DEFAULT_FILTERS : false;
    const notebooks = this.props.notebooks;
    const listNotebooks = () => {
      return (
        <table className="table table-hover table-responsive">
          <tbody>
          {NotebookHeader()}
          {notebooks
            .filter(
              (notebook: NotebookModel) =>
                (!this.props.showDeleted && isLive(notebook)) || (this.props.showDeleted && !isLive(notebook)))
            .map(
            (notebook: NotebookModel) =>
              <Notebook
                key={notebook.unique_name}
                notebook={notebook}
                onDelete={() => this.props.onDelete(notebook.unique_name)}
                onStop={() => this.props.onStop(notebook.unique_name)}
                onArchive={() => this.props.onArchive(notebook.unique_name)}
                onRestore={() => this.props.onRestore(notebook.unique_name)}
                showBookmarks={this.props.showBookmarks}
                bookmark={() => this.props.bookmark(notebook.unique_name)}
                unbookmark={() => this.props.unbookmark(notebook.unique_name)}
              />)}
          </tbody>
        </table>
      );
    };

    let empty: any;
    if (this.props.endpointList === BOOKMARKS) {
      empty = EmptyBookmarks(
        this.props.isCurrentUser,
        'notebook',
        'notebook');
    } else if (this.props.endpointList === ARCHIVES) {
       empty = EmptyArchives(
        this.props.isCurrentUser,
        'notebook',
        'notebook');
    } else {
      empty = EmptyList(
        this.props.isCurrentUser,
        'notebook',
        'notebook',
        'polyaxon run --help');
    }

    return (
      <PaginatedTable
        count={this.props.count}
        componentList={listNotebooks()}
        componentEmpty={empty}
        filters={filters}
        fetchData={this.props.fetchData}
        fetchSearches={this.props.fetchSearches}
        createSearch={this.props.createSearch}
        deleteSearch={this.props.deleteSearch}
        sortOptions={DEFAULT_SORT_OPTIONS}
        filterOptions={JOB_FILTER_OPTIONS}
      />
    );
  }
}
