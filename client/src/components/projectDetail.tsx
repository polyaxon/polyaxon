import * as React from 'react';
import * as _ from 'lodash';
import * as moment from 'moment';
import { Tab, TabPane, Nav, NavItem, Col, Row } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

import { ProjectModel } from '../models/project';
import Experiments from '../containers/experiments';
import Groups from '../containers/groups';
import { getUserUrl } from '../constants/utils';

export interface Props {
  project: ProjectModel;
  onDelete: (project: ProjectModel) => any;
  fetchData: () => any;
}

export default class ProjectDetail extends React.Component<Props, Object> {
  componentDidMount() {
    const {project, onDelete, fetchData} = this.props;
    fetchData();
  }

  public render() {
    let state = {experimentCurrentPage: 0};

    const handleNextPage = () => {
      state.experimentCurrentPage += 1;
    };

    const handlePreviousPage = () => {
      state.experimentCurrentPage -= 1;
    };

    const {project, onDelete, fetchData} = this.props;
    if (_.isNil(project)) {
      return (<div>Nothing</div>);
    }
    let visibility = project.is_public ? 'Public' : 'Private';
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <span className="title">
              <i className="fa fa-server icon" aria-hidden="true"/>
              <LinkContainer to={getUserUrl(project.user)}>
                <span>
                  <a className="title">
                    {project.user}
                  </a>/
                </span>
              </LinkContainer>
              <span className="title">
                {project.name}
              </span>
            </span>
            <div className="meta-description">
              {project.description}
            </div>
            <div className="meta">
              <span className="meta-info">
                <i className="fa fa-lock icon" aria-hidden="true"/>
                <span className="title">Visibility:</span>
                {visibility}
              </span>
              <span className="meta-info">
                <i className="fa fa-clock-o icon" aria-hidden="true"/>
                <span className="title">Last updated:</span>
                {moment(project.updated_at).fromNow()}
              </span>
              <span className="meta-info">
                <i className="fa fa-cube icon" aria-hidden="true"/>
                <span className="title">Experiments:</span>
                {project.num_experiments}
              </span>
              <span className="meta-info">
                <i className="fa fa-cubes icon" aria-hidden="true"/>
                <span className="title">Experiment Groups:</span>
                {project.num_experiment_groups}
              </span>
            </div>
          </div>
          <Tab.Container defaultActiveKey={1} id="project-tabs" className="plx-nav">
            <Row className="clearfix">
              <Col sm={12}>
                <Nav bsStyle="tabs">
                  <NavItem eventKey={1}>Independent Experiments</NavItem>
                  <NavItem eventKey={2}>Experiment groups</NavItem>
                </Nav>
              </Col>
              <Col sm={12}>
                <Tab.Content animation={true} mountOnEnter={true}>
                  <Tab.Pane eventKey={1}>
                    <Experiments
                      fetchData={() => null}
                      user={project.user}
                      projectName={project.unique_name}
                      currentPage={state.experimentCurrentPage}
                    />
                  </Tab.Pane>
                  <Tab.Pane eventKey={2}>
                     <Groups fetchData={() => null} user={project.user} projectName={project.unique_name}/>
                  </Tab.Pane>
                </Tab.Content>
              </Col>
            </Row>
          </Tab.Container>

        </div>
      </div>
    );
  }
}
