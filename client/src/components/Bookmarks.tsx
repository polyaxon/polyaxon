import * as React from 'react';

import { getUserUrl, getBookmarksUrl } from '../constants/utils';
import Breadcrumb from './breadcrumb';
import LinkedTab from './linkedTab';
import BuildInstructions from './instructions/buildInstructions';

export interface Props {
  user: string;
}

export default class Bookmarks extends React.Component<Props, Object> {
  public render() {
    let bookmarksUrl = getBookmarksUrl(this.props.user);

    return (
      <div className="row">
        <div className="col-md-12">
          <Breadcrumb
            icon="fa-star"
            links={[
              {name: this.props.user, value: getUserUrl(this.props.user)},
              {name: 'bookmarks'}]}
          />
          <LinkedTab
            baseUrl={bookmarksUrl}
            tabs={[
              {
                title: 'Experiments',
                // component: <Experiments user={this.props.user}/>,
                component: <BuildInstructions id={1} />,
                relUrl: 'experiments'
              }, {
                title: 'Experiment groups',
                // component: <Groups user={this.props.user}/>,
                component: <BuildInstructions id={1} />,
                relUrl: 'groups'
              }, {
                title: 'Jobs',
                // component: <Jobs user={this.props.user}/>,
                component: <BuildInstructions id={1} />,
                relUrl: 'jobs'
              }, {
                title: 'Builds',
                // component: <Builds user={this.props.user}/>,
                component: <BuildInstructions id={1} />,
                relUrl: 'builds'
              }, {
                title: 'Projects',
                // component: <Projects user={this.props.user}/>,
                component: <BuildInstructions id={1} />,
                relUrl: 'Projects'
              }
            ]}
          />
        </div>
      </div>
    );
  }
}
