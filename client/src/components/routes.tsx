import * as React from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';

import { getHomeUrl } from '../constants/utils';
import Archives from '../containers/archives';
import Bookmarks from '../containers/bookmarks';
import BuildCreate from '../containers/builds/buildCreate';
import BuildDetail from '../containers/builds/buildDetail';
import ExperimentJobDetail from '../containers/experimentJobs/experimentJobDetail';
import ExperimentCreate from '../containers/experiments/experimentCreate';
import ExperimentDetail from '../containers/experiments/experimentDetail';
import GroupCreate from '../containers/groups/groupCreate';
import GroupDetail from '../containers/groups/groupDetail';
import HealthStatus from '../containers/healthStatus';
import JobCreate from '../containers/jobs/jobCreate';
import JobDetail from '../containers/jobs/jobDetail';
import NotebookCreate from '../containers/notebooks/notebookCreate';
import NotebookDetail from '../containers/notebooks/notebookDetail';
import ProjectCreate from '../containers/projects/projectCreate';
import ProjectDetail from '../containers/projects/projectDetail';
import TensorboardCreate from '../containers/tensorboards/tensorboardCreate';
import TensorboardDetail from '../containers/tensorboards/tensorboardDetail';
import Token from '../containers/token';
import User from '../containers/user';
import ClusterActivityLogs from './activitylogs/clusterActivityLogs';
import HistoryLogs from './activitylogs/histroyLogs';

function Routes() {
  const tokenRoute = '/app/token/';
  const statusRoute = '/app/status/';
  const clusterActivityLogsRoute = '/app/activitylogs/';
  const historyLogsRoute = '/app/historylogs/';
  const newProjectRoute = '/app/projects/new/';
  const userRoute = '/app/:user/';
  const bookmarksRoute = '/app/bookmarks/:user/';
  const archivesRoute = '/app/archives/:user/';
  const projectDetailRoute = '/app/:user/:projectName/';
  const buildDetailRoute = '/app/:user/:projectName/builds/:buildId/';
  const newBuildRoute = '/app/:user/:projectName/builds/new/';
  const notebookDetailRoute = '/app/:user/:projectName/notebooks/:notebookId/';
  const newNotebookRoute = '/app/:user/:projectName/notebooks/new/';
  const tensorboardDetailRoute = '/app/:user/:projectName/tensorboards/:tensorboardId/';
  const newProjectTensorboardRoute = '/app/:user/:projectName/tensorboards/new/';
  const jobDetailRoute = '/app/:user/:projectName/jobs/:jobId/';
  const newJobRoute = '/app/:user/:projectName/jobs/new/';
  const newExperimentTensorboardRoute = '/app/:user/:projectName/experiments/:experimentId/tensorboards/new/';
  const newExperimentRoute = '/app/:user/:projectName/experiments/new/';
  const experimentDetailRoute = '/app/:user/:projectName/experiments/:experimentId/';
  const newGroupRoute = '/app/:user/:projectName/groups/new/';
  const groupDetailRoute = '/app/:user/:projectName/groups/:groupId/';
  const newGroupTensorboardRoute = '/app/:user/:projectName/groups/:groupId/tensorboards/new/';
  const experimentJobDetailRoute = '/app/:user/:projectName/experiments/:experimentId/jobs/:jobId/';

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
      <Route path={statusRoute} component={HealthStatus}/>
      <Route path={historyLogsRoute} component={HistoryLogs}/>
      <Route path={clusterActivityLogsRoute} component={ClusterActivityLogs}/>
      <Route path={newProjectRoute} component={ProjectCreate}/>
      <Route path={experimentJobDetailRoute} component={ExperimentJobDetail}/>
      <Route path={newBuildRoute} component={BuildCreate}/>
      <Route path={buildDetailRoute} component={BuildDetail}/>
      <Route path={newNotebookRoute} component={NotebookCreate}/>
      <Route path={notebookDetailRoute} component={NotebookDetail}/>
      <Route path={newProjectTensorboardRoute} component={TensorboardCreate}/>
      <Route path={tensorboardDetailRoute} component={TensorboardDetail}/>
      <Route path={newJobRoute} component={JobCreate}/>
      <Route path={jobDetailRoute} component={JobDetail}/>
      <Route path={newGroupRoute} component={GroupCreate}/>
      <Route path={newGroupTensorboardRoute} component={TensorboardCreate}/>
      <Route path={groupDetailRoute} component={GroupDetail}/>
      <Route path={newExperimentRoute} component={ExperimentCreate}/>
      <Route path={newExperimentTensorboardRoute} component={TensorboardCreate}/>
      <Route path={experimentDetailRoute} component={ExperimentDetail}/>
      <Route path={bookmarksRoute} component={Bookmarks}/>
      <Route path={archivesRoute} component={Archives}/>
      <Route path={projectDetailRoute} component={ProjectDetail}/>
      <Route path={userRoute} component={User}/>

      <Route path="*" render={() => <Redirect to={getHomeUrl()}/>}/>
    </Switch>
  );
}

export default Routes;
