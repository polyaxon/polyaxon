import * as React from "react";
import {Switch, Redirect, Route} from "react-router-dom";

import ProjectDetail from "../containers/projectDetail";
import ExperimentDetail from "../containers/experimentDetail";
import GroupDetail from "../containers/groupDetail";
import JobDetail from "../containers/jobDetail";
import Projects from "../containers/projects";


function Routes() {
  return (
    <Switch>
        <Route path="/:user/:projectName/experiments/:experimentSequence/jobs/:jobSequence/" component={JobDetail} />
        <Route path="/:user/:projectName/groups/:groupSequence/" component={GroupDetail} />
        <Route path="/:user/:projectName/experiments/:experimentSequence/" component={ExperimentDetail} />
        <Route path="/:user/:projectName/" component={ProjectDetail} />
        <Route path="/:user" component={Projects}/>
        <Redirect from="*" to="/admin"/>
    </Switch>
  )
}

export default Routes;
