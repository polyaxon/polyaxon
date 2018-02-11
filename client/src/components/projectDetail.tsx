import * as React from 'react';
import * as _ from 'lodash';
import * as moment from 'moment';
import { Tab, Nav, NavItem, Col, Row, Pager } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

import { ProjectModel } from '../models/project';
import Experiments from '../containers/experiments';
import Groups from '../containers/groups';
import { getUserUrl } from '../constants/utils';

export interface Props {
  project: ProjectModel;
  onDelete: (project: ProjectModel) => undefined;
  fetchData: () => undefined;
}

interface State {
  experimentCurrentPage: number;
}

export default class ProjectDetail extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {experimentCurrentPage: 1};
  }

  componentDidMount() {
    const {project, onDelete, fetchData} = this.props;
    fetchData();
  }

  handleNextPage = () => {
      this.setState((prevState, props) => ({
        experimentCurrentPage: prevState.experimentCurrentPage + 1,
      }));
  }

  handlePreviousPage = () => {
      this.setState((prevState, props) => ({
        experimentCurrentPage: prevState.experimentCurrentPage - 1,
      }));
  }

  public render() {
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
                      user={project.user}
                      projectName={project.unique_name}
                      currentPage={this.state.experimentCurrentPage}
                    />
                    <Pager>
                      <Pager.Item onClick={this.handlePreviousPage}>Previous</Pager.Item>{' '}
                      <Pager.Item onClick={this.handleNextPage}>Next</Pager.Item>
                    </Pager>
                  </Tab.Pane>
                  <Tab.Pane eventKey={2}>
                    <Groups user={project.user} projectName={project.unique_name}/>
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
