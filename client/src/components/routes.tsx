import * as React from "react";
import {Switch, Redirect, Route} from "react-router-dom";

import Experiments from "../containers/experiments";
import Projects from "../containers/projects";
import ProjectDetail from "../containers/projectDetail";


const Home = () => (
  <div>
    <h2>Home</h2>
  </div>
);

const About = () => (
  <div>
    <h2>About</h2>
  </div>
);

function Routes() {
  return (
    <Switch>
        <Route exact path="/" component={Home}/>
        <Route exact path="/projects" component={Projects}/>
        <Route path="/projects/:projectId(\\d+)" component={ProjectDetail} />
        <Route exact path="/experiments" component={Experiments}/>
        <Route path="/about" component={About}/>
        <Redirect from="*" to="/"/>
    </Switch>
  )
}

export default Routes;
