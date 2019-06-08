import * as React from 'react';
import { Route, Switch } from 'react-router-dom';

import BuildCreate from '../containers/builds/buildCreate';
import BuildDetail from '../containers/builds/buildDetail';
import Builds from '../containers/builds/builds';
import ExperimentJobDetail from '../containers/experimentJobs/experimentJobDetail';
import ExperimentCreate from '../containers/experiments/experimentCreate';
import ExperimentDetail from '../containers/experiments/experimentDetail';
import Experiments from '../containers/experiments/experiments';
import GroupCreate from '../containers/groups/groupCreate';
import GroupDetail from '../containers/groups/groupDetail';
import Groups from '../containers/groups/groups';
import JobCreate from '../containers/jobs/jobCreate';
import JobDetail from '../containers/jobs/jobDetail';
import Jobs from '../containers/jobs/jobs';
import NotebookCreate from '../containers/notebooks/notebookCreate';
import NotebookDetail from '../containers/notebooks/notebookDetail';
import Notebooks from '../containers/notebooks/notebooks';
import ProjectDetail from '../containers/projects/projectDetail';
import TensorboardCreate from '../containers/tensorboards/tensorboardCreate';
import TensorboardDetail from '../containers/tensorboards/tensorboardDetail';
import Tensorboards from '../containers/tensorboards/tensorboards';

const ProjectRoutes = () => {
    const projectDetailRoute = '/app/:user/:projectName/details/';

    const experimentDetailRoute = '/app/:user/:projectName/experiments/:experimentId/';
    const newExperimentTensorboardRoute = '/app/:user/:projectName/experiments/:experimentId/tensorboards/new/';
    const newProjectExperimentRoute = '/app/:user/:projectName/experiments/new/';
    const projectExperimentsRoute = '/app/:user/:projectName/experiments/';
    const experimentJobDetailRoute = '/app/:user/:projectName/experiments/:experimentId/jobs/:jobId/';

    const newProjectGroupRoute = '/app/:user/:projectName/groups/new/';
    const groupDetailRoute = '/app/:user/:projectName/groups/:groupId/';
    const newGroupTensorboardRoute = '/app/:user/:projectName/groups/:groupId/tensorboards/new/';
    const groupExperimentsRoute = '/app/:user/:projectName/groups/:groupId/experiments/';
    const projectGroupsRoute = '/app/:user/:projectName/groups/';

    const buildDetailRoute = '/app/:user/:projectName/builds/:buildId/';
    const projectBuildsRoute = '/app/:user/:projectName/builds/';
    const newProjectBuildRoute = '/app/:user/:projectName/builds/new/';

    const notebookDetailRoute = '/app/:user/:projectName/notebooks/:notebookId/';
    const projectNotebooksRoute = '/app/:user/:projectName/notebooks/';
    const newProjectNotebookRoute = '/app/:user/:projectName/notebooks/new/';

    const tensorboardDetailRoute = '/app/:user/:projectName/tensorboards/:tensorboardId/';
    const projectTensorboardsRoute = '/app/:user/:projectName/tensorboards/';
    const newProjectTensorboardRoute = '/app/:user/:projectName/tensorboards/new/';

    const newProjectJobRoute = '/app/:user/:projectName/jobs/new/';
    const jobDetailRoute = '/app/:user/:projectName/jobs/:jobId/';
    const projectJobsRoute = '/app/:user/:projectName/jobs/';

    return (
        <Switch>
            <Route
                exact={true}
                path={projectBuildsRoute}
                component={() => <Builds showBookmarks={true} useFilters={true}/>}
            />
            <Route
                exact={true}
                path={projectJobsRoute}
                component={() => <Jobs showBookmarks={true} useFilters={true}/>}
            />
            <Route
                exact={true}
                path={projectNotebooksRoute}
                component={() => <Notebooks showBookmarks={true} useFilters={true}/>}
            />
            <Route
                exact={true}
                path={projectTensorboardsRoute}
                component={() => <Tensorboards showBookmarks={true} useFilters={true}/>}
            />
            <Route
                exact={true}
                path={projectGroupsRoute}
                component={() => <Groups showBookmarks={true} useFilters={true}/>}
            />
            <Route
                exact={true}
                path={[projectExperimentsRoute, groupExperimentsRoute]}
                component={() => <Experiments showBookmarks={true} useCheckbox={true} useFilters={true}/>}
            />
            <Route
                exact={true}
                path={experimentJobDetailRoute}
                component={ExperimentJobDetail}
            />

            /* Build */
            <Route
                exact={true}
                path={buildDetailRoute}
                component={BuildDetail}
            />
            <Route
                exact={true}
                path={newProjectBuildRoute}
                component={BuildCreate}
            />

            /* Notebook */
            <Route
                exact={true}
                path={notebookDetailRoute}
                component={NotebookDetail}
            />
            <Route
                exact={true}
                path={newProjectNotebookRoute}
                component={NotebookCreate}
            />

            /* Tensorboards */
            <Route
                exact={true}
                path={tensorboardDetailRoute}
                component={TensorboardDetail}
            />

            /* Jobs */
            <Route
                exact={true}
                path={newProjectJobRoute}
                component={JobCreate}
            />
            <Route
                exact={true}
                path={jobDetailRoute}
                component={JobDetail}
            />
            <Route
                exact={true}
                path={jobDetailRoute}
                component={JobDetail}
            />

            /* Groups */
            <Route
                exact={true}
                path={newProjectGroupRoute}
                component={GroupCreate}
            />
            <Route
                exact={true}
                path={groupDetailRoute}
                component={GroupDetail}
            />
            <Route
                exact={true}
                path={newGroupTensorboardRoute}
                component={TensorboardCreate}
            />

            /* Experiments */
            <Route
                exact={true}
                path={newProjectExperimentRoute}
                component={ExperimentCreate}
            />
            <Route
                exact={true}
                path={experimentDetailRoute}
                component={ExperimentDetail}
            />
            <Route
                exact={true}
                path={newExperimentTensorboardRoute}
                component={TensorboardCreate}
            />

            /* Projects */
            <Route
                exact={true}
                path={projectDetailRoute}
                component={ProjectDetail}
            />
            <Route
                exact={true}
                path={newProjectTensorboardRoute}
                component={TensorboardCreate}
            />
        </Switch>
    );
};

export default ProjectRoutes;
