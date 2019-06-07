import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/notebooks';
import { isDone } from '../../constants/statuses';
import { getNotebookApiUrl, getProjectUrl, getUserUrl, splitUniqueName, } from '../../constants/utils';
import Statuses from '../../containers/statuses';
import { BookmarkInterface } from '../../interfaces/bookmarks';
import { NotebookModel } from '../../models/notebook';
import { getBookmark } from '../../utils/bookmarks';
import Breadcrumb from '../breadcrumb';
import YamlText from '../editors/yamlText';
import { EmptyList } from '../empty/emptyList';
import NotebookInstructions from '../instructions/notebookInstructions';
import LinkedTab from '../linkedTab';
import NotebookActions from './notebookActions';
import NotebookOverview from './notebookOverview';

export interface Props {
  notebook: NotebookModel;
  onUpdate: (updateDict: { [key: string]: any }) => actions.NotebookAction;
  onDelete: () => actions.NotebookAction;
  onArchive: () => actions.NotebookAction;
  onRestore: () => actions.NotebookAction;
  onStop: () => actions.NotebookAction;
  fetchData: () => actions.NotebookAction;
  bookmark: () => actions.NotebookAction;
  unbookmark: () => actions.NotebookAction;
}

export default class NotebookDetail extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const notebook = this.props.notebook;
    if (_.isNil(notebook)) {
      return EmptyList(false, 'notebook', 'notebook');
    }

    const bookmark: BookmarkInterface = getBookmark(
      this.props.notebook.bookmarked, this.props.bookmark, this.props.unbookmark);
    const values = splitUniqueName(notebook.project);
    const notebookUrl = getNotebookApiUrl(values[0], values[1], this.props.notebook.id);
    const projectUrl = getProjectUrl(values[0], values[1]);
    const breadcrumbLinks = [
      {name: values[0], value: getUserUrl(values[0])},
      {name: values[1], value: projectUrl},
      {name: 'Notebooks', value: `${projectUrl}#notebooks`},
      {name: `Notebook ${notebook.id}`}];
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <Breadcrumb
              icon="fas fa-gavel"
              links={breadcrumbLinks}
              bookmark={bookmark}
              actions={
                <NotebookActions
                  onDelete={this.props.onDelete}
                  onStop={this.props.onStop}
                  onArchive={notebook.deleted ? undefined : this.props.onArchive}
                  onRestore={notebook.deleted ? this.props.onRestore : undefined}
                  isRunning={!isDone(this.props.notebook.last_status)}
                  pullRight={true}
                />
              }
            />
            <LinkedTab
              baseUrl={notebookUrl}
              tabs={[
                {
                  title: 'Overview',
                  component: <NotebookOverview
                    notebook={notebook}
                    onUpdate={this.props.onUpdate}
                    onFetch={this.props.fetchData}
                  />,
                  relUrl: ''
                }, {
                  title: 'Statuses',
                  component: <Statuses
                    project={notebook.project}
                    resource="notebooks"
                    id={notebook.id}
                  />,
                  relUrl: 'statuses'
                }, {
                  title: 'Config',
                  component: <YamlText title="Config" configText={notebook.content}/>,
                  relUrl: 'config'
                }, {
                  title: 'Instructions',
                  component: <NotebookInstructions id={notebook.id}/>,
                  relUrl: 'instructions'
                }
              ]}
            />
          </div>
        </div>
      </div>
    );
  }
}
