import * as React from "react";
import {Switch, Redirect, Route} from "react-router-dom";

import Experiments from "../containers/experiments";
import Jobs from "../containers/jobs";

import Projects from "../containers/projects";


function Routes() {
  return (
    <Switch>
        <Route exact path="/admin" component={Projects}/>
        <Route path="/admin/:projectName/experiments/:experimentSequence/jobs" component={Jobs} />
        <Route path="/admin/:projectName/experiments" component={Experiments} />
        <Redirect from="*" to="/admin"/>
    </Switch>
  )
}

export default Routes;
