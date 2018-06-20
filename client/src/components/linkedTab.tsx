import * as React from 'react';
import { Tab, Nav, NavItem, Col, Row } from 'react-bootstrap';

import './linkedTab.less';

export interface Props {
  baseUrl: string;
  tabs: Array<{ title: string, component: React.ReactNode, relUrl: string }>;
}

function LinkedTab({baseUrl, tabs}: Props) {
  let getActiveTab = () => {
    let pieces = location.hash.split('?')[0].split('#');
    if (pieces.length === 1) {
      return 1;
    }
    let activeTab: string = pieces[1];
    let eventKey = 1;
    for (let tab of tabs) {
      if (tab.relUrl === activeTab) {
        break;
      }
      eventKey++;
    }
    return eventKey;
  };

  return (
    <Tab.Container defaultActiveKey={getActiveTab()} className="tab-container">
      <Row className="clearfix">
        <Col sm={12}>
          <Nav bsStyle="tabs">
            {tabs.map((tab, idx) =>
              <NavItem eventKey={idx + 1} href={`${baseUrl}#${tab.relUrl}`} key={idx}>{tab.title}</NavItem>
            )}
          </Nav>
          <Tab.Content animation={true} mountOnEnter={true}>
            {tabs.map((tab, idx) =>
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

export default LinkedTab;
