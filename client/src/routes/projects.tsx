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
import {
    buildDetailURL,
    experimentDetailsURL,
    experimentJobDetailURL,
    groupDetailURL,
    groupExperimentsURL,
    jobDetailURL,
    newExperimentTensorboardURL,
    newGroupTensorboardURL,
    newProjectBuildURL,
    newProjectExperimentURL,
    newProjectGroupURL,
    newProjectJobURL,
    newProjectNotebookURL,
    newProjectTensorboardURL,
    notebookDetailURL,
    projectBuildsURL,
    projectDetailURL,
    projectExperimentsURL,
    projectGroupsURL,
    projectJobsURL,
    projectNotebooksURL,
    projectTensorboardsURL,
    tensorboardDetailURL
} from '../urls/routes/projects';

const ProjectRoutes = () => {
    return (
        <Switch>
            <Route
                exact={true}
                path={projectBuildsURL}
                component={() => <Builds showBookmarks={true} useFilters={true}/>}
            />
            <Route
                exact={true}
                path={projectJobsURL}
                component={() => <Jobs showBookmarks={true} useFilters={true}/>}
            />
            <Route
                exact={true}
                path={projectNotebooksURL}
                component={() => <Notebooks showBookmarks={true} useFilters={true}/>}
            />
            <Route
                exact={true}
                path={projectTensorboardsURL}
                component={() => <Tensorboards showBookmarks={true} useFilters={true}/>}
            />
            <Route
                exact={true}
                path={projectGroupsURL}
                component={() => <Groups showBookmarks={true} useFilters={true}/>}
            />
            <Route
                exact={true}
                path={[projectExperimentsURL, groupExperimentsURL]}
                component={() => <Experiments showBookmarks={true} useCheckbox={true} useFilters={true}/>}
            />
            <Route
                exact={true}
                path={experimentJobDetailURL}
                component={ExperimentJobDetail}
            />

            /* Build */
            <Route
                exact={true}
                path={buildDetailURL}
                component={BuildDetail}
            />
            <Route
                exact={true}
                path={newProjectBuildURL}
                component={BuildCreate}
            />

            /* Notebook */
            <Route
                exact={true}
                path={notebookDetailURL}
                component={NotebookDetail}
            />
            <Route
                exact={true}
                path={newProjectNotebookURL}
                component={NotebookCreate}
            />

            /* Tensorboards */
            <Route
                exact={true}
                path={tensorboardDetailURL}
                component={TensorboardDetail}
            />

            /* Jobs */
            <Route
                exact={true}
                path={newProjectJobURL}
                component={JobCreate}
            />
            <Route
                exact={true}
                path={jobDetailURL}
                component={JobDetail}
            />

            /* Groups */
            <Route
                exact={true}
                path={newProjectGroupURL}
                component={GroupCreate}
            />
            <Route
                exact={true}
                path={groupDetailURL}
                component={GroupDetail}
            />
            <Route
                exact={true}
                path={newGroupTensorboardURL}
                component={TensorboardCreate}
            />

            /* Experiments */
            <Route
                exact={true}
                path={newProjectExperimentURL}
                component={ExperimentCreate}
            />
            <Route
                exact={true}
                path={experimentDetailsURL}
                component={ExperimentDetail}
            />
            <Route
                exact={true}
                path={newExperimentTensorboardURL}
                component={TensorboardCreate}
            />

            /* Projects */
            <Route
                exact={true}
                path={projectDetailURL}
                component={ProjectDetail}
            />
            <Route
                exact={true}
                path={newProjectTensorboardURL}
                component={TensorboardCreate}
            />
        </Switch>
    );
};

export default ProjectRoutes;
