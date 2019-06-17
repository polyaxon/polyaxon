import * as React from 'react';
import { Route, Switch } from 'react-router-dom';
import BuildCreate from '../containers/builds/buildCreate';
import ExperimentCreate from '../containers/experiments/experimentCreate';
import GroupCreate from '../containers/groups/groupCreate';
import JobCreate from '../containers/jobs/jobCreate';
import NotebookCreate from '../containers/notebooks/notebookCreate';
import ProjectCreate from '../containers/projects/projectCreate';
import TensorboardCreate from '../containers/tensorboards/tensorboardCreate';
import {
  newBuildUrl,
  newExperimentUrl,
  newGroupUrl,
  newJobUrl,
  newNotebookUrl,
  newProjectUrl,
  newTensorboardUrl
} from '../urls/routes/new';

const NewEntityRoutes = () => {
  return (
    <Switch>
      <Route path={newProjectUrl} component={ProjectCreate}/>
      <Route path={newExperimentUrl} component={ExperimentCreate}/>
      <Route path={newGroupUrl} component={GroupCreate}/>
      <Route path={newJobUrl} component={JobCreate}/>
      <Route path={newBuildUrl} component={BuildCreate}/>
      <Route path={newNotebookUrl} component={NotebookCreate}/>
      <Route path={newTensorboardUrl} component={TensorboardCreate}/>
    </Switch>
  );
};

export default NewEntityRoutes;
