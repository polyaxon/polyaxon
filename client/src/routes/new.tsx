import * as React from 'react';
import { Route, Switch } from 'react-router-dom';
import BuildCreate from '../containers/builds/buildCreate';
import ExperimentCreate from '../containers/experiments/experimentCreate';
import GroupCreate from '../containers/groups/groupCreate';
import JobCreate from '../containers/jobs/jobCreate';
import NotebookCreate from '../containers/notebooks/notebookCreate';
import ProjectCreate from '../containers/projects/projectCreate';
import TensorboardCreate from '../containers/tensorboards/tensorboardCreate';

const NewEntityRoutes = () => {
  const newProjectRoute = '/app/new/project/';
  const newExperimentRoute = '/app/new/experiment/';
  const newGroupRoute = '/app/new/group/';
  const newJobRoute = '/app/new/job/';
  const newBuildRoute = '/app/new/build/';
  const newNotebookRoute = '/app/new/notebook/';
  const newTensorboardRoute = '/app/new/tensorboard/';

  return (
    <Switch>
      <Route path={newProjectRoute} component={ProjectCreate}/>
      <Route path={newExperimentRoute} component={ExperimentCreate}/>
      <Route path={newGroupRoute} component={GroupCreate}/>
      <Route path={newJobRoute} component={JobCreate}/>
      <Route path={newBuildRoute} component={BuildCreate}/>
      <Route path={newNotebookRoute} component={NotebookCreate}/>
      <Route path={newTensorboardRoute} component={TensorboardCreate}/>
    </Switch>
  );
};

export default NewEntityRoutes;
