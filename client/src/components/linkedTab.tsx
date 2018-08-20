import * as React from 'react';
import { Col, Nav, NavItem, Row, Tab } from 'react-bootstrap';

import './linkedTab.less';

export interface Props {
  baseUrl: string;
  tabs: Array<{ title: string, component: React.ReactNode, relUrl: string }>;
  tabId?: string;
}

export default class LinkedTab extends React.Component<Props, Object> {
  public render() {
    const tabId = this.props.tabId ? this.props.tabId : Math.floor((Math.random() * 100) + 1).toString();
    const getActiveTab = () => {
      const pieces = location.hash.split('?')[0].split('#');
      if (pieces.length === 1) {
        return 1;
      }
      const activeTab: string = pieces[1];
      let eventKey = 1;
      for (const tab of this.props.tabs) {
        if (tab.relUrl === activeTab) {
          break;
        }
        eventKey++;
      }
      return eventKey;
    };

    return (
      <Tab.Container id={tabId} defaultActiveKey={getActiveTab()} className="tab-container">
        <Row className="clearfix">
          <Col sm={12}>
            <Nav bsStyle="tabs">
              {this.props.tabs.map((tab, idx) =>
                <NavItem eventKey={idx + 1} href={`${this.props.baseUrl}#${tab.relUrl}`} key={idx}>{tab.title}</NavItem>
              )}
            </Nav>
            <Tab.Content animation={true} mountOnEnter={true}>
              {this.props.tabs.map((tab, idx) =>
                <Tab.Pane eventKey={idx + 1} key={idx}>
                  {tab.component}
                </Tab.Pane>
              )}
            </Tab.Content>
          </Col>
        </Row>
      </Tab.Container>
    );
  }
}
