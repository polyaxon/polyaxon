import * as React from 'react';
import { Switch, Redirect, Route } from 'react-router-dom';

import ProjectDetail from '../containers/projectDetail';
import ExperimentDetail from '../containers/experimentDetail';
import GroupDetail from '../containers/groupDetail';
import JobDetail from '../containers/jobDetail';
import Projects from '../containers/projects';
import Token from '../containers/token';

import { getHomeUrl } from '../constants/utils';

function Routes() {
  let tokenRoute = '/app/token';
  let projectDetailRoute = '/app/:user/:projectName/';
  let projectsRoute = '/app/:user/';
  let experimentDetailRoute = '/app/:user/:projectName/experiments/:experimentId/';
  let groupDetailRoute = '/app/:user/:projectName/groups/:groupId/';
  let jobDetailRoute = '/app/:user/:projectName/experiments/:experimentId/jobs/:jobId/';

  /**
   * in the future if we want to reactivate login redirection we can do something like this:
   *       <Route
   *         path={jobDetailRoute}
   *         render={() => (
   *           isUserAuthenticated() ? (
   *             <Route path={jobDetailRoute} component={JobDetail}/>
   *           ) : (
   *             <Route component={({}, {}) => window.location.replace(getLoginUrl(true))} />;
   *           )
   *         )}
   *       />
   */

  return (
    <Switch>
      <Route path={tokenRoute} component={Token}/>
      <Route path={jobDetailRoute} component={JobDetail}/>
      <Route path={groupDetailRoute} component={GroupDetail}/>
      <Route path={experimentDetailRoute} component={ExperimentDetail}/>
      <Route path={projectDetailRoute} component={ProjectDetail}/>
      <Route path={projectsRoute} component={Projects}/>

      <Route path="*" render={() => <Redirect to={getHomeUrl()}/>}/>
    </Switch>
  );
}

export default Routes;
